import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

class MapService():
    def get_stories(lat, long, stories):
        url = 'http://www.mapquestapi.com/search/v2/radius'
        params = {
            'key': os.environ.get('MAPQUEST_KEY')
        }
        data = {
            'origin': {
                'latLng': {
                    'lat': float(lat),
                    'lng': float(long)
                }
            },
            'options': {
                'maxMatches': 100,
                'radius': 25,
                'units': 'm'
            },
            'remoteDataList': stories
        }
        response = requests.post(url, params=params, data=json.dumps(data, indent=1))
        return response.json()

    def get_directions(request, story):
        url = 'http://www.mapquestapi.com/directions/v2/route'
        params = {
            'key': os.environ.get('MAPQUEST_KEY'),
            'from': f"{request['latitude']},{request['longitude']}",
            'to': f'{story.latitude},{story.longitude}'
        }
        response = requests.post(url, params=params)
        return response.json()

    def get_distance(lat, long, story_lat, story_long):
        url = 'http://www.mapquestapi.com/directions/v2/route'
        params = {
            'key': os.environ.get('MAPQUEST_KEY'),
            'from': f'{float(lat)},{float(long)}',
            'to': f'{story_lat},{story_long}'
            }
        response = requests.get(url, params=params)
        parsed = response.json()['route']
        if parsed['routeError']['errorCode'] == -400:
            return parsed['distance']
        else:
            return 'Impossible route.'
