import pytest
from message_in_a_bottle.quickstart.models import Story
from django.test import TestCase

@pytest.mark.django_db
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.story = Story.objects.create(title= 'My Story', message= 'I said hi.', latitude= 41.599143847185175, longitude= -87.89309819798746)

    def test_create_dict(self):
        story = {
            "id": 1,
            "title": 'My Cool Story',
            "message": 'I once saw a really pretty flower.',
            "latitude": 123.456892,
            "longitude": -19.982791
        }

        assert Story.create_dict(story) == {
            "key": 1,
            "title": 'My Cool Story',
            "shapePoints": [
                123.456892, -19.982791
            ]
        }

    def test_map_stories(self):
        self.story
        assert Story.map_stories() ==[]
