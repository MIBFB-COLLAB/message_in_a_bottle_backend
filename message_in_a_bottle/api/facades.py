from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.services import MapService

class MapFacade():
  def get_stories(request):
    response = MapService.get_stories(request['latitude'], request['longitude'], Story.map_stories())
    results = [] if response['resultsCount'] == 0 else response['searchResults']
    city_state = MapService.get_city_state(request['latitude'], request['longitude'])
    return [results, city_state]

  def get_city_state(request):
    return MapService.get_city_state(request['latitude'], request['longitude'])

  def get_distance(request, story):
      response = MapService.get_distance(
                    request['latitude'],
                    request['longitude'],
                    story.latitude,
                    story.longitude
                 )
      route_result = response['route']['routeError']['errorCode']
      return response['route']['distance'] if route_result == -400 else 'Impossible route.'

  def get_directions(request, story):
      response = MapService.get_directions(request, story)['route']
      return 'Impossible route.' if response['routeError']['errorCode'] == 2 else response
