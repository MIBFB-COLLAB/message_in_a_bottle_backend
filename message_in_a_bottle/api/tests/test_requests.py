import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
class TestGetStory:
    def test_db_setup(self):
        assert Story.objects.count() == 0
        self.story_dict = {
            'title': 'My Cool Story',
            'message': 'I once saw a really pretty flower.',
            'latitude': 123.456892,
            'longitude': -19.982791
        }
        self.new_story = Story.objects.create(
            title = self.story_dict['title'],
            message = self.story_dict['message'],
            latitude = self.story_dict['latitude'],
            longitude = self.story_dict['longitude']
        )
        assert Story.objects.count() == 1

    def test_get_existing_story(self):
        TestGetStory.test_db_setup(self)

        self.valid_id = Story.objects.latest('id').id
        self.route = f'/api/v1/stories/{self.valid_id}'

        client = APIClient()
        response = client.get(self.route)
        serializer = StorySerializer(Story.objects.get(pk=self.valid_id))

        assert response.status_code == 200
        assert response.data['data'] == serializer.data

    def test_get_non_existent_story(self):
        TestGetStory.test_db_setup(self)

        self.invalid_id = Story.objects.latest('id').id + 1
        self.route = f'/api/v1/stories/{self.invalid_id}'

        client = APIClient()
        response = client.get(self.route)

        assert response.status_code == 404
