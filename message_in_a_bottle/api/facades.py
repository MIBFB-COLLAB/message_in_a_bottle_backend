from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.services import MapService

class MapFacade():
  def get_stories(latitude, longitude):
    response = MapService.get_stories(latitude, longitude, Story.map_stories())
    results = [] if response['resultsCount'] == 0 else response['searchResults']
    city_state = MapService.get_city_state(latitude, longitude)
    return [results, city_state]
  
  def get_city_state(request):
    return MapService.get_city_state(request.data['latitude'], request.data['longitude'])

  def get_distance(request, story):
    return MapService.get_distance(
                request.query_params['latitude'],
                request.query_params['longitude'],
                story.latitude,
                story.longitude
            )
            