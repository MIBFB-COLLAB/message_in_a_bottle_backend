import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

class MapService():
    def get_stories(lat, long, stories):
        url = 'http://www.mapquestapi.com/search/v2/radius'
        params = {
            "key": os.environ.get('MAPQUEST_KEY')
        }
        data = {
          "origin": {
            "latLng": {
              "lat": lat,
              "lng": long
            }
          },
          "options": {
            "maxMatches": 100,
            "radius": 25,
            "units": "m"
          },
        "remoteDataList": stories
          }
        response = requests.post(url, params=params, data=json.dumps(data, indent = 1))
        return response.json()
