import pytest
from message_in_a_bottle.api.models import Story
from django.test import TestCase
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        Story.objects.create(title= 'My Story', message= 'I said hi.', latitude= 41.599143847185175, longitude= -87.89309819798746)

    def test_create_dict(self):
        TestModels.setUpTestData()
        story = Story.objects.all()[0]

        assert Story.create_dict(story) == {
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
        valid_coords = {'lat': 23.563729, 'long': -145.782}
        invalid_coords = {'lat': 230.563729, 'long': -1450.782}

        assert Story.validate_user_coords(valid_coords) == True
        assert Story.validate_user_coords(invalid_coords) == False

    def test_validation_error_raised_lat_or_long(self):
        story = Story(title= 'My Story', message= 'I said hi.', latitude= 123.599143847185175, longitude= -200.89309819798746)
        with self.assertRaises(ValidationError):
            story.save()
            story.full_clean()
