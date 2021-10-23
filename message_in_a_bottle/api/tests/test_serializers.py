import pytest
from django.test import TestCase
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
class TestStorySerializer(TestCase):
    @classmethod
    def test_db_setup(cls):
        assert Story.objects.count() == 0
        cls.story_dict = {
            'title': 'My Cool Story',
            'message': 'I once saw a really pretty flower.',
            'latitude': 123.456892,
            'longitude': -19.982791
        }
        cls.new_story = Story.objects.create(
            title = cls.story_dict['title'],
            message = cls.story_dict['message'],
            latitude = cls.story_dict['latitude'],
            longitude = cls.story_dict['longitude']
        )
        assert Story.objects.count() == 1

    def test_serializer_reformat(self):
        TestStorySerializer.test_db_setup()
        self.story = Story.objects.latest('id')

        serializer = StorySerializer(self.story)

        assert type(self.story) == Story
        assert serializer.reformat(self.story.__dict__) == {
            'id': self.story.id,
            'type': self.story.__class__.__name__,
            'attributes': {
                'name': self.story.name,
                'title': self.story.title,
                'message': self.story.message,
                'latitude': self.story.latitude,
                'longitude': self.story.longitude,
                'location': self.story.location,
                'created_at': self.story.created_at,
                'updated_at': self.story.updated_at
            }
        }

    def test_serializer_coordinates_error(self):
        self.expected = {
            'coordinates': [
                'Invalid latitude or longitude.'
            ]
        }
        self.actual = StorySerializer.coords_error()

        assert self.actual == self.expected

    def test_serializer_blank_coordinates(self):
        self.expected = {
            'coordinates': [
                "Latitude or longitude can't be blank."
            ]
        }
        self.actual = StorySerializer.blank_coords()

        assert self.actual == self.expected
