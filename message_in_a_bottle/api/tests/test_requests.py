import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
class TestStoryRequests(TestCase):
    @classmethod
    def test_db_setup(cls, return_dict=False):
        assert Story.objects.count() == 0
        cls.story_dict = {
            'title': 'My Cool Story',
            'message': 'I once saw a really pretty flower.',
            'longitude': 123.456892,
            'latitude': -19.982791
        }
        cls.new_story = Story.objects.create(
            title = cls.story_dict['title'],
            message = cls.story_dict['message'],
            latitude = cls.story_dict['latitude'],
            longitude = cls.story_dict['longitude']
        )
        assert Story.objects.count() == 1
        if return_dict:
            return cls.story_dict

    def test_get_existing_story(self):
        TestStoryRequests.test_db_setup()

        self.valid_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.valid_id}'

        client = APIClient()
        response = client.get(self.route)
        serializer = StorySerializer(Story.objects.get(pk=self.valid_id))

        assert response.status_code == 200
        assert response.data['data'] == serializer.reformat(serializer.data)

    def test_get_non_existent_story(self):
        TestStoryRequests.test_db_setup()

        self.invalid_id = Story.objects.latest('id').id + 1
        self.route = f'/api/v1/stories/{self.invalid_id}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 404

    def test_create_valid_story(self):
        self.story_dict = TestStoryRequests.test_db_setup(return_dict=True)
        self.route = '/api/v1/stories'

        client = APIClient()
        response = client.post(self.route, self.story_dict, format='json')
        story_id = response.data['data']['id']
        serializer = StorySerializer(Story.objects.get(pk=story_id))

        assert response.status_code == 201
        assert response.data['data'] == serializer.reformat(serializer.data)
        assert Story.objects.count() == 2

    def test_create_empty_story(self):
        self.route = '/api/v1/stories'

        client = APIClient()
        response = client.post(self.route, {}, format='json')
        errors = response.data['errors']

        assert response.status_code == 400
        assert errors['coordinates'] == ['Invalid latitude or longitude.']

    def delete_existing_story(self):
        TestStoryRequests.test_db_setup()

        self.story_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.story_id}'

        client = APIClient()
        response = client.delete(self.route)

        assert response.status_code == 204
