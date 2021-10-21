import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
class TestGetStory(TestCase):
    @classmethod
    def test_db_setup(cls):
        assert Story.objects.count() == 0
        cls.story_dict = {
            'title': 'Union Station',
            'message': 'I once saw a really pretty flower.',
            'latitude': 39.75711894267296,
            'longitude': -105.00325615707887
        }
        cls.new_story = Story.objects.create(
            title = cls.story_dict['title'],
            message = cls.story_dict['message'],
            latitude = cls.story_dict['latitude'],
            longitude = cls.story_dict['longitude']
        )

        Story.objects.create(
            title = "Gates Crescent Park",
            message = "Took a walk",
            latitude = 39.749379471614546,
            longitude = -105.01696456480278
        )

        Story.objects.create(
            title = "Gates Crescent Park",
            message = "Took a walk",
            latitude = 39.749379471614546,
            longitude = -105.01696456480278
        )

        Story.objects.create(
            title = "Botanic Gardens",
            message = "Smelled a rose",
            latitude = 39.733903355068456,
            longitude = -104.95994497497446
        )

        Story.objects.create(
            title = "DIA",
            message = "I landed from a trip",
            latitude = 39.865426458967676,
            longitude = -104.67452255667705
        )

        assert Story.objects.count() == 5

    def test_get_existing_story(self):
        TestGetStory.test_db_setup()

        self.valid_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.valid_id}'

        client = APIClient()
        response = client.get(self.route)
        serializer = StorySerializer(Story.objects.get(pk=self.valid_id))

        assert response.status_code == 200
        assert response.data['data'] == serializer.data

    def test_get_non_existent_story(self):
        TestGetStory.test_db_setup()

        self.invalid_id = Story.objects.latest('id').id + 1
        self.route = f'/api/v1/stories/{self.invalid_id}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 404

    def test_get_story_index(self):
        TestGetStory.test_db_setup()
        self.lat = 39.74822614190254
        self.long = -104.99898275758112
        self.route = f'/api/v1/stories?lat={self.lat}&long={self.long}'

        client = APIClient()
        response = client.get(self.route)
        assert response.status_code == 200
        assert response.data['data'].__class__.__name__ == 'dict'
        assert 'input_location' in response.data['data'].keys()
        assert 'stories' in response.data['data'].keys()
        assert response.data['data']['stories'].__class__.__name__ == 'list'
        assert response.data['data']['stories']

    def test_error_no_stories_in_range(self):
        TestGetStory.test_db_setup()
        self.lat = 34.134529719319424
        self.long = -118.29851756023974
        self.route = f'/api/v1/stories?lat={self.lat}&long={self.long}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 200
        assert response.data['data'].__class__.__name__ == 'dict'
        assert 'input_location' in response.data['data'].keys()
        assert 'stories' in response.data['data'].keys()
        assert response.data['data']['stories'].__class__.__name__ == 'list'
        assert not response.data['data']['stories']

    def test_error_invalid_coordinates(self):
        TestGetStory.test_db_setup()
        self.lat = 340.134529719319424
        self.long = -1180.29851756023974
        self.route = f'/api/v1/stories?lat={self.lat}&long={self.long}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 400
        assert response.data['errors'] == 'Invalid latitude and longitude'

    def test_error_no_coordinates(self):
        TestGetStory.test_db_setup()
        self.route = f'/api/v1/stories'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 400
        assert response.data['errors'] == 'Invalid latitude and longitude'

    def test_story_does_not_save_invalid_lat_long(self):
        TestGetStory.test_db_setup()
        dict = {
            "title": "I'm invalid",
            "message": "Delete me I'm invalid!",
            "latitude": 450.8762,
            "longitude": 960.12893,
            "location": 'place'
        }
        original_length = len(Story.objects.all())
        self.route = f'/api/v1/stories'

        client = APIClient()
        response = client.post(self.route, dict, format='json')

        assert original_length == len(Story.objects.all())

    def test_story_saves_valid_lat_long(self):
        TestGetStory.test_db_setup()
        dict = {
            "title": "I'm valid",
            "message": "Keep me I'm valid!",
            "latitude": 45.8762,
            "longitude": 96.12893,
            "location": 'place'
        }
        original_length = len(Story.objects.all())
        self.route = f'/api/v1/stories'

        client = APIClient()
        response = client.post(self.route, dict, format='json')

        assert len(Story.objects.all()) == original_length + 1
