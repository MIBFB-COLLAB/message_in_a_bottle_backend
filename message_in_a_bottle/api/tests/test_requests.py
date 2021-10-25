import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
class TestStoryRequests(TestCase):
    """
    Database transactional fixture setup for test runs:
    """
    @classmethod
    def test_db_setup(cls, return_dict=False):
        assert Story.objects.count() == 0
        cls.story_dict = {
            'title': 'Union Station',
            'message': 'I once saw a really pretty flower.',
            'latitude': 39.757118942673,
            'longitude': -105.003256157079
        }
        cls.new_story = Story.objects.create(
            title = cls.story_dict['title'],
            message = cls.story_dict['message'],
            latitude = cls.story_dict['latitude'],
            longitude = cls.story_dict['longitude']
        )
        Story.objects.create(
            title = 'Gates Crescent Park',
            message = 'Took a walk',
            latitude = 39.749379471614546,
            longitude = -105.01696456480278
        )
        Story.objects.create(
            title = 'Botanic Gardens',
            message = 'Smelled a rose',
            latitude = 39.733903355068456,
            longitude = -104.95994497497446
        )
        Story.objects.create(
            title = 'DIA',
            message = 'I landed from a trip',
            latitude = 39.865426458967676,
            longitude = -104.67452255667705
        )
        assert Story.objects.count() == 4
        if return_dict:
            return cls.story_dict

    """
    Retrieve a story instance:
    """
    def test_get_existing_story(self):
        self.story_dict = TestStoryRequests.test_db_setup(return_dict=True)

        self.valid_id = Story.objects.latest('id').id
        self.lat = self.story_dict['latitude']
        self.long = self.story_dict['longitude']
        self.route = f'/api/v1/stories/{self.valid_id}?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)
        serializer = StorySerializer(Story.objects.get(pk=self.valid_id))
        distance = response.data['data']['attributes']['distance_in_miles']

        assert response.status_code == 200
        assert response.data['data'] == serializer.reformat(serializer.data, distance)

    def test_get_story_impossible_route(self):
        TestStoryRequests.test_db_setup()

        self.valid_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.valid_id}?latitude={0}&longitude={0}'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ['Impossible route.']

    def test_get_story_invalid_coordinates(self):
        TestStoryRequests.test_db_setup()

        self.valid_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.valid_id}?latitude={100000}&longitude={100000}'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ['Invalid latitude or longitude.']

    def test_get_story_empty_params(self):
        TestStoryRequests.test_db_setup()

        self.valid_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.valid_id}?latitude=&longitude='

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ["Latitude or longitude can't be blank."]

    def test_get_story_no_params(self):
        TestStoryRequests.test_db_setup()

        self.valid_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.valid_id}'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ["Latitude or longitude can't be blank."]

    def test_get_non_existent_story(self):
        TestStoryRequests.test_db_setup()

        self.invalid_id = Story.objects.latest('id').id + 1
        self.route = f'/api/v1/stories/{self.invalid_id}?latitude={0}&longitude={0}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 404

    """
    Create a story:
    """
    def test_create_valid_story(self):
        self.story_dict = TestStoryRequests.test_db_setup(return_dict=True)
        self.route = '/api/v1/stories'

        client = APIClient()
        response = client.post(self.route, self.story_dict, format='json')
        story_id = response.data['data']['id']
        serializer = StorySerializer(Story.objects.get(pk=story_id))

        assert response.status_code == 201
        assert response.data['data'] == serializer.reformat(serializer.data)
        assert Story.objects.count() == 5

    def test_create_empty_story(self):
        self.invalid_dict = {}
        self.route = '/api/v1/stories'

        client = APIClient()
        response = client.post(self.route, self.invalid_dict, format='json')
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ["Latitude or longitude can't be blank."]

    def test_create_story_invalid_coordinates(self):
        self.invalid_dict = {
            'title': "I'm invalid",
            'message': 'My coordinates are invalid!',
            'latitude': 450.8762,
            'longitude': 960.12893
        }
        self.route = f'/api/v1/stories'

        client = APIClient()
        response = client.post(self.route, self.invalid_dict, format='json')
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ['Invalid latitude or longitude.']

    """
    Delete a story instance:
    """
    def test_delete_existing_story(self):
        TestStoryRequests.test_db_setup()

        self.story_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.story_id}'

        client = APIClient()
        response = client.delete(self.route)
        assert response.status_code == 204

    """
    Update a story instance:
    """
    def test_valid_update_existing_story(self):
        self.story_dict = TestStoryRequests.test_db_setup(return_dict=True)
        self.story = Story.objects.earliest('id')
        self.route = f'/api/v1/stories/{self.story.id}'
        assert self.story.title == self.story_dict['title']

        client = APIClient()
        response = client.patch(self.route, {'title': 'An even cooler story'}, format='json')
        serializer = StorySerializer(Story.objects.get(pk=self.story.id))

        assert response.status_code == 200
        assert response.data['data'] == serializer.reformat(serializer.data)

        self.story = Story.objects.latest('id')
        assert self.story.title != self.story_dict['title']

    def test_invalid_update_existing_story(self):
        TestStoryRequests.test_db_setup()

        self.story_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.story_id}'

        client = APIClient()
        response = client.patch(self.route, {}, format='json')
        serializer = StorySerializer(Story.objects.get(pk=self.story_id))

        self.story = Story.objects.latest('id')
        assert self.story.name != ''
        assert self.story.title != ''
        assert self.story.message != ''
        assert self.story.latitude != ''
        assert self.story.longitude != ''

    """
    List all stories:
    """
    def test_get_story_index(self):
        TestStoryRequests.test_db_setup()

        self.lat = 39.74822614190254
        self.long = -104.99898275758112
        self.route = f'/api/v1/stories?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 200
        assert response.data['data'].__class__.__name__ == 'dict'
        assert 'input_location' in response.data['data'].keys()
        assert 'stories' in response.data['data'].keys()
        assert response.data['data']['stories'].__class__.__name__ == 'list'
        assert response.data['data']['stories']

    def test_error_no_stories_in_range(self):
        TestStoryRequests.test_db_setup()

        self.lat = 34.134529719319424
        self.long = -118.29851756023974
        self.route = f'/api/v1/stories?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 200
        assert response.data['data'].__class__.__name__ == 'dict'
        assert 'input_location' in response.data['data'].keys()
        assert 'stories' in response.data['data'].keys()
        assert response.data['data']['stories'].__class__.__name__ == 'list'
        assert not response.data['data']['stories']

    def test_error_invalid_coordinates(self):
        TestStoryRequests.test_db_setup()

        self.lat = 340.134529719319424
        self.long = -1180.29851756023974
        self.route = f'/api/v1/stories?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ['Invalid latitude or longitude.']

    def test_get_stories_blank_coordinates(self):
        TestStoryRequests.test_db_setup()

        self.lat = ''
        self.long = ''
        self.route = f'/api/v1/stories?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ["Latitude or longitude can't be blank."]

    def test_get_stories_no_coordinates(self):
        TestStoryRequests.test_db_setup()

        self.route = f'/api/v1/stories'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['messages'] == ["Latitude or longitude can't be blank."]

    """
    Get directions to a single story:
    """
    def test_get_directions(self):
        TestStoryRequests.test_db_setup()

        story = Story.objects.all()[0]
        self.lat = 34.134529719319424
        self.long = -118.29851756023974
        self.route = f'/api/v1/stories/{story.id}/directions?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 200
        assert isinstance(response.data['data'], list)
        assert isinstance(response.data['data'][0], dict)
        assert 'id' in response.data['data'][0].keys()
        assert 'type' in response.data['data'][0].keys()
        assert response.data['data'][0]['type'] == 'directions'
        assert 'attributes' in response.data['data'][0].keys()
        assert isinstance(response.data['data'][0]['attributes'], dict)
        assert 'narrative' in response.data['data'][0]['attributes'].keys()
        assert 'distance' in response.data['data'][0]['attributes'].keys()

    def test_get_directions_impossible_route(self):
        TestStoryRequests.test_db_setup()

        story = Story.objects.all()[0]
        self.lat = 21.393936208637445
        self.long = -157.8674605018104
        self.route = f'/api/v1/stories/{story.id}/directions?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['message'] == ['Impossible route.']

    def test_get_directions_invalid_coordinates(self):
        TestStoryRequests.test_db_setup()

        story = Story.objects.all()[0]
        self.lat = 210.393936208637445
        self.long = -1570.8674605018104
        self.route = f'/api/v1/stories/{story.id}/directions?latitude={self.lat}&longitude={self.long}'

        client = APIClient()
        response = client.get(self.route)
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['coordinates'] == ['Invalid latitude or longitude.']
