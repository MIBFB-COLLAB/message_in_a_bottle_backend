import pytest
import pprint
pp = pprint.PrettyPrinter(indent=2)
from message_in_a_bottle.api.services import MapService
from django.test import TestCase

class TestServices(TestCase):
    def test_get_stories(self):
        lat = 39.74822614190254
        long = -104.99898275758112
        stories = [
            {
            "key": "1",
            "name": "Union Station",
            "shapePoints": [
                39.75711894267296,
                -105.00325615707887
                ]
            },
            {
            "key": "2",
            "name": "Gates Crescent Park",
            "shapePoints": [
                39.749379471614546,
                -105.01696456480278
                ]
            },
            {
            "key": "3",
            "name": "Botanic Gardens",
            "shapePoints": [
                39.733903355068456,
                -104.95994497497446
                ]
            },
            {
            "key": "4",
            "name": "DIA",
            "shapePoints": [
                39.865426458967676,
                -104.67452255667705
                ]
            }
        ]

        response = MapService.get_stories(lat, long, stories)

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
        user_location = {
            'lat': 39.749379471614546,
            'long': -105.01696456480278
        }
        story = {
            'lat': 39.75711894267296,
            'long': -105.00325615707887
        }
        response = MapService.get_distance(
            user_location['lat'],
            user_location['long'],
            story['lat'],
            story['long']
        )

        assert 'route' in response.keys()
        assert 'distance' in response['route'].keys()

