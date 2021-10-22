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
    
    def get_distance(lat, long, story_lat, story_long):
      url = 'http://www.mapquestapi.com/directions/v2/route'
      params = {
        "key": os.environ.get('MAPQUEST_KEY'),
        "from": f"{lat},{long}",
        "to": f"{story_lat},{story_long}"
      }
      response = requests.get(url, params=params)
      return response.json()['route']['distance']