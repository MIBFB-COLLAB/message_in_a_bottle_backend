import pytest
from message_in_a_bottle.api.models import Story
from django.test import TestCase
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        Story.objects.create(title= 'My Story', message= 'I said hi.', latitude= 41.599143847185175, longitude= -87.89309819798746)

    def test_mapquest_data_dict(self):
        TestModels.setUpTestData()
        story = Story.objects.all()[0]

        assert Story.mapquest_data_dict(story) == {
            "key": str(story.id),
            "name": story.title,
            "shapePoints": [
                story.latitude, story.longitude
            ]
        }

    def test_map_stories(self):
        story = Story.objects.all()[0]

        assert len(Story.objects.all()) == 1

        assert Story.map_stories() ==[{
            'key': str(story.id),
            'name': story.title,
            'shapePoints': [
                story.latitude, story.longitude
            ]}
        ]

    def test_valid_user_coords(self):
        valid_coords = {'latitude': 23.563729, 'longitude': -145.782}
        invalid_coords = {'latitude': 230.563729, 'longitude': -1450.782}

        assert Story.valid_coords(valid_coords) == True
        assert Story.valid_coords(invalid_coords) == False
