import pprint
pp = pprint.PrettyPrinter(indent=2)
import os
import json
import pytest
import requests
from requests_mock.mocker import Mocker
from django.test import TestCase
from message_in_a_bottle.api.services import MapService
from message_in_a_bottle.api.models import Story

class TestServices(TestCase):
    def test_get_stories(self):
        self.base_path = os.path.dirname(__file__)
        self.fixture = f'{self.base_path}/fixtures/radius_response.json'
        with open(self.fixture, 'r') as reader:
            json_blob = json.load(reader)

        self.user_location = {
            'latitude': 39.749379471614546,
            'longitude': -105.01696456480278
        }
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

        with Mocker() as mocker:
            mocker.post(MapService.base_urls()['radius'], json=json_blob, status_code=200)
            response = MapService.get_stories(
                self.user_location['latitude'],
                self.user_location['longitude'],
                self.stories
            )

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

    def test_get_directions(self):
        self.base_path = os.path.dirname(__file__)
        self.fixture = f'{self.base_path}/fixtures/route_response.json'
        with open(self.fixture, 'r') as reader:
            json_blob = json.load(reader)

        self.user_location = {
            'latitude': 39.749379471614546,
            'longitude': -105.01696456480278
        }
        self.story = Story.objects.create(
            title = 'Gates Crescent Park',
            message = 'Took a walk',
            latitude = 39.75711894267296,
            longitude = -105.00325615707887
        )

        with Mocker() as mocker:
            mocker.post(MapService.base_urls()['route'], json=json_blob, status_code=200)
            response = MapService.get_directions(self.user_location, self.story)

        assert 'distance' in response['route'].keys()
        assert 'legs' in response['route'].keys()
        assert isinstance(response['route']['legs'], list)
        assert 'maneuvers' in response['route']['legs'][0].keys()
        assert isinstance(response['route']['legs'][0]['maneuvers'], list)

    def test_get_distance(self):
        self.base_path = os.path.dirname(__file__)
        self.fixture = f'{self.base_path}/fixtures/route_response.json'
        with open(self.fixture, 'r') as reader:
            json_blob = json.load(reader)

        self.user_location = {
            'lat': 39.749379471614546,
            'long': -105.01696456480278
        }
        self.story_location = {
            'lat': 39.75711894267296,
            'long': -105.00325615707887
        }

        # with Mocker() as mocker:
        #     mocker.get(MapService.base_urls()['route'], json=json_blob, status_code=200)
        #     response = MapService.get_distance(
        #         self.user_location['lat'],
        #         self.user_location['long'],
        #         self.story_location['lat'],
        #         self.story_location['long']
        #     )

        response = MapService.get_distance(
            self.user_location['lat'],
            self.user_location['long'],
            self.story_location['lat'],
            self.story_location['long']
        )

        assert type(response) == dict

    def test_get_valid_city_state(self):
        self.base_path = os.path.dirname(__file__)
        self.fixture = f'{self.base_path}/fixtures/valid_geocode_response.json'
        with open(self.fixture, 'r') as reader:
            json_blob = json.load(reader)

        self.user_location = {
            'lat': 40.337408,
            'long': -104.9460736
        }
        self.expected = 'Weld, CO'

        with Mocker() as mocker:
            mocker.get(MapService.base_urls()['reverse_geocode'], json=json_blob, status_code=200)
            response = MapService.get_city_state(
                self.user_location['lat'],
                self.user_location['long']
            )
        assert response == self.expected

    def test_get_invalid_city_state(self):
        self.base_path = os.path.dirname(__file__)
        self.fixture = f'{self.base_path}/fixtures/invalid_geocode_response.json'
        with open(self.fixture, 'r') as reader:
            json_blob = json.load(reader)

        self.hope_you_brought_water_wings = {
            'lat': 0,
            'long': 0
        }
        self.expected = ''

        with Mocker() as mocker:
            mocker.get(MapService.base_urls()['reverse_geocode'], json=json_blob, status_code=200)
            response = MapService.get_city_state(
                self.hope_you_brought_water_wings['lat'],
                self.hope_you_brought_water_wings['long']
            )
        assert response == self.expected
