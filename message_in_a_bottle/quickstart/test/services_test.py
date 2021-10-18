import pytest
from message_in_a_bottle.quickstart.services import MapService
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

        assert MapService.get_stories(lat, long, stories) == True