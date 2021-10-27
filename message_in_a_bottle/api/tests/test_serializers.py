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

    def test_reformat(self):
        TestStorySerializer.test_db_setup()
        self.story = Story.objects.latest('id')

        serializer = StorySerializer(self.story)

        assert type(self.story) == Story
        assert serializer.reformat(self.story.__dict__, 1.25) == {
            'id': self.story.id,
            'type': str(self.story.__class__.__name__).lower(),
            'attributes': {
                'name': self.story.name,
                'title': self.story.title,
                'message': self.story.message,
                'latitude': self.story.latitude,
                'longitude': self.story.longitude,
                'location': self.story.location,
                'created_at': self.story.created_at,
                'updated_at': self.story.updated_at,
                'distance_in_miles': 1.25
            }
        }

    def test_stories_index(self):
        self.expected = {
            'input_location': 'Denver, CO',
            'stories': []
        }
        self.actual = StorySerializer.stories_index([], 'Denver, CO')

        assert self.actual == self.expected

    def test_story_directions(self):
        TestStorySerializer.test_db_setup()
        self.story = Story.objects.latest('id')
        self.manuever = {'narrative': 'Turn left on Pecos St.', 'distance': 2}
        self.directions_obj = {
            'id': None,
            'type': 'directions',
            'attributes': {
                'narrative': 'Turn left on Pecos St.',
                'distance': '2 miles'
            }
        }

        assert StorySerializer.format_directions(self.manuever) == self.directions_obj

    def test_coords_error_invalid_coords(self):
        self.expected = {
            'messages': [
                'Invalid latitude or longitude.'
            ],
            'code': 1
        }
        self.actual = StorySerializer.coords_error({'latitude': 999999, 'longitude': 9999999})

        assert self.actual == self.expected

    def test_coords_error_missing_coords(self):
        self.expected = {
            'messages': [
                "Latitude or longitude can't be blank."
            ],
            'code': 1
        }
        self.actual = StorySerializer.coords_error({})

        assert self.actual == self.expected

    def test_coords_error_impossible_route(self):
        self.expected = {
            'messages': [
                'Impossible route.'
            ],
            'code': 2
        }
        self.actual = StorySerializer.coords_error('Impossible route.')

        assert self.actual == self.expected

    def test_coords_error_no_error(self):
        self.expected = {
            'messages': [],
            'code': 0
        }
        self.actual = StorySerializer.coords_error({'latitude': 40.05506, 'longitude': -105.0066986})

        assert self.actual == self.expected
