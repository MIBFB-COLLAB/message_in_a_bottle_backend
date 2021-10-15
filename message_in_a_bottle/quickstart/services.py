import request

def get_stories(lat, long, stories):
    url = 'http://www.mapquestapi.com/search/v2/radius'
    params = {
        "key": MAPQUEST_KEY
    }
    data = {
      "origin": {
        "latLng": {
          "lat": 39.74822614190254,
          "lng": -104.99898275758112
        }
      },
      "options": {
        "maxMatches": 5,
        "radius": 10,
        "units": "m"
      },
    "remoteDataList": stories
      }
     ]
    }
    response = requests.post(url, params=params, data=data)
    stories = response.json()
