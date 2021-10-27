import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

class MapService():
    def base_urls():
        return {
            'radius': 'http://www.mapquestapi.com/search/v2/radius',
            'route': 'http://www.mapquestapi.com/directions/v2/route',
            'reverse_geocode': 'http://www.mapquestapi.com/geocoding/v1/reverse'
        }

    def api_key():
        return os.environ.get('MAPQUEST_KEY')

    def get_stories(lat, long, stories):
        url = MapService.base_urls()['radius']
        params = {
            'key': MapService.api_key()
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
                'radius': 50,
                'units': 'm'
            },
            'remoteDataList': stories
        }
        response = requests.post(url, params=params, data=json.dumps(data, indent=1))
        return response.json()

    def get_directions(request, story):
        url = MapService.base_urls()['route']
        params = {
            'key': MapService.api_key(),
            'from': f"{request['latitude']},{request['longitude']}",
            'to': f'{story.latitude},{story.longitude}',
            'manMaps': False
        }
        response = requests.post(url, params=params)
        return response.json()

    def get_distance(lat, long, story_lat, story_long):
        url = MapService.base_urls()['route']
        params = {
            'key': MapService.api_key(),
            'from': f'{float(lat)},{float(long)}',
            'to': f'{story_lat},{story_long}',
            'manMaps': False
        }
        response = requests.get(url, params=params)
        import pdb; pdb.set_trace()
        if response.status_code != 403:
            return response.json()
        else:
            return {'route': {'distance': 'exceeded rate limite', 'routeError': {'errorCode': 403}}}
    def get_city_state(lat, long):
        url = MapService.base_urls()['reverse_geocode']
        params = {
            'key': MapService.api_key(),
            'location': f'{float(lat)},{float(long)}',
            'thumbMaps': False
        }
        response = requests.get(url, params=params)
        parsed = response.json()['results'][0]['locations'][0]
        concatenated = f"{parsed['adminArea4']}, {parsed['adminArea3']}"
        return concatenated if concatenated != ', ' else ''
