import pytest
from message_in_a_bottle.quickstart.models import Story
from django.test import TestCase

@pytest.mark.django_db
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        Story.objects.create(title= 'My Story', message= 'I said hi.', latitude= 41.599143847185175, longitude= -87.89309819798746)

    def test_create_dict(self):
        TestModels.setUpTestData()
        story = Story.objects.all()[0]

        assert Story.create_dict(story) == {
            "key": story.id,
            "title": story.title,
            "shapePoints": [
                story.latitude, story.longitude
            ]
        }

    def test_map_stories(self):
        story = Story.objects.all()[0]

        assert len(Story.objects.all()) == 1

        assert Story.map_stories() ==[{
                'key': story.id,
                'title': story.title,
                'shapePoints': [
                    story.latitude, story.longitude
                ]}
            ]
