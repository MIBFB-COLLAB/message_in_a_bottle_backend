import pytest
from django.test import TestCase
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
class TestStorySerializer(TestCase):
    @classmethod
    def test_db_setup(cls, return_dict=False):
        assert Story.objects.count() == 0
        cls.story_dict = {
            'title': 'My Cool Story',
            'message': 'I once saw a really pretty flower.',
            'latitude': 40.05506,
            'longitude': -105.0066986
        }
        Story.objects.create(
            title = cls.story_dict['title'],
            message = cls.story_dict['message'],
            latitude = cls.story_dict['latitude'],
            longitude = cls.story_dict['longitude']
        )
        Story.objects.create(
            title = 'Hello',
            message = 'World',
            latitude = cls.story_dict['latitude'] + 0.1,
            longitude = cls.story_dict['longitude']
        )
        assert Story.objects.count() == 2
        if return_dict:
            return cls.story_dict

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
            'code': 1,
            'messages': [
                'Invalid latitude or longitude.'
            ]
        }
        self.actual = StorySerializer.coords_error({'latitude': 999999, 'longitude': 9999999})

        assert self.actual == self.expected

    # def test_stories_near_user(self):
    #     self.story_dict = TestStorySerializer.test_db_setup(return_dict=True)
    #     self.lat = self.story_dict['latitude']
    #     self.long = self.story_dict['longitude']
    #
    #     self.actual = StorySerializer.stories_near_user(self.lat, self.long, Story.objects.all())
    #
    #     assert isinstance(self.actual, list)
    #     assert len(self.actual) == 2
    #     assert self.actual[0]['attributes']['title'] == self.story_dict['title']
    #     assert self.actual[1]['attributes']['title'] == 'Hello'

    # def test_no_stories_near_user(self):
    #     TestStorySerializer.test_db_setup()
    #     self.lat = 0
    #     self.long = 0
    #
    #     self.actual = StorySerializer.stories_near_user(self.lat, self.long, Story.objects.all())
    #
    #     assert isinstance(self.actual, list)
    #     assert len(self.actual) == 0

    def test_stories_index(self):
        TestStorySerializer.test_db_setup()

        self.actual = StorySerializer.stories_index(Story.objects.all(), 'Boulder, CO')

        assert isinstance(self.actual, dict)
        assert self.actual['input_location'] == 'Boulder, CO'
        assert len(self.actual['stories']) == 2
