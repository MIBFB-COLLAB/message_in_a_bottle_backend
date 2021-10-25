import pprint
pp = pprint.PrettyPrinter(indent=2)
import pytest
from django.test import TestCase
from message_in_a_bottle.api.services import MapService
from message_in_a_bottle.api.models import Story

class TestServices(TestCase):
    def test_get_directions(self):
        self.lat = 39.74822614190254
        self.long = -104.99898275758112
        self.story = Story.objects.create(
            title = 'Gates Crescent Park',
            message = 'Took a walk',
            latitude = 39.749379471614546,
            longitude = -105.01696456480278
        )

        self.request = {
            'latitude': self.lat,
            'longitude': self.long
        }
        response = MapService.get_directions(self.request, self.story)

        assert 'distance' in response['route'].keys()
        assert 'legs' in response['route'].keys()
        assert response['route']['legs'].__class__.__name__ == 'list'
        assert 'maneuvers' in response['route']['legs'][0].keys()
        assert response['route']['legs'][0]['maneuvers'].__class__.__name__ == 'list'

    def test_get_stories(self):
        self.lat = 39.74822614190254
        self.long = -104.99898275758112
        self.stories = [
            {
            'key': '1',
            'name': 'Union Station',
            'shapePoints': [
                39.75711894267296,
                -105.00325615707887
                ]
            },
            {
            'key': '2',
            'name': 'Gates Crescent Park',
            'shapePoints': [
                39.749379471614546,
                -105.01696456480278
                ]
            },
            {
            'key': '3',
            'name': 'Botanic Gardens',
            'shapePoints': [
                39.733903355068456,
                -104.95994497497446
                ]
            },
            {
            'key': '4',
            'name': 'Griffith Observatory',
            'shapePoints': [
                34.13912518423296,
                -118.31225791576566
                ]
            }
        ]

        response = MapService.get_stories(self.lat, self.long, self.stories)

        assert response['resultsCount'] == 3
        assert 'origin' in response.keys()
        assert 'searchResults' in response.keys()
        assert len(response['searchResults']) == 3

        assert 'name' in response['searchResults'][0]
        assert 'distance' in response['searchResults'][0]
        assert 'distanceUnit' in response['searchResults'][0]
        assert 'shapePoints' in response['searchResults'][0]

        assert response['searchResults'][0]['name'] == 'Union Station'
        assert response['searchResults'][0]['distanceUnit'] == 'm'

    def test_get_distance(self):
        self.user_location = {
            'lat': 39.749379471614546,
            'long': -105.01696456480278
        }
        self.story = {
            'lat': 39.75711894267296,
            'long': -105.00325615707887
        }
        response = MapService.get_distance(
            self.user_location['lat'],
            self.user_location['long'],
            self.story['lat'],
            self.story['long']
        )

        assert type(response) == float

    def test_get_valid_city_state(self):
        self.user_location = {
            'lat': 39.749379471614546,
            'long': -105.01696456480278
        }

        self.actual = MapService.get_city_state(
            self.user_location['lat'],
            self.user_location['long']
        )
        self.expected = 'Denver, CO'

        assert self.actual == self.expected

    def test_get_invalid_city_state(self):
        self.hope_you_brought_water_wings = {
            'lat': 0,
            'long': 0
        }

        self.actual = MapService.get_city_state(
            self.hope_you_brought_water_wings['lat'],
            self.hope_you_brought_water_wings['long']
        )
        self.expected = ''

        assert self.actual == self.expected
