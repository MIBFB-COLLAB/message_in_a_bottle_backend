import requests
import os
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
            "maxMatches": 5,
            "radius": 10,
            "units": "m"
          },
        "remoteDataList": stories
          }
        response = requests.post(url, params=params, data=data)
        stories = response.json()
