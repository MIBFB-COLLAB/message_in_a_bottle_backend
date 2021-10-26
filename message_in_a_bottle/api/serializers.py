from rest_framework import serializers
from .models import Story
from message_in_a_bottle.api.services import MapService
from message_in_a_bottle.api.facades import MapFacade

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'latitude', 'longitude', 'message', 'name', 'title', 'location', 'created_at', 'updated_at']

    def reformat(self, story_dict, return_distance=None):
        output_dict = {
            'id': story_dict['id'],
            'type': 'story',
            'attributes': {
                'name': story_dict['name'],
                'title': story_dict['title'],
                'message': story_dict['message'],
                'latitude': story_dict['latitude'],
                'longitude': story_dict['longitude'],
                'location': story_dict['location'],
                'created_at': story_dict['created_at'],
                'updated_at': story_dict['updated_at']
            }
        }
        if return_distance is not None:
            output_dict['attributes']['distance_in_miles'] = return_distance
        return output_dict

    def stories_index_serializer(response, city_state):
        stories = map(StorySerializer.reformat_mapquest_response, response)
        return {
            'input_location': city_state,
            'stories': list(stories)
        }

    def reformat_mapquest_response(story):
        return {
            'id': story['key'],
            'type': 'story',
            'attributes': {
                'title': story['name'],
                'distance_in_miles': story['distance'],
                'latitude': story['shapePoints'][0],
                'longitude': story['shapePoints'][1]
            }
        }

    def story_directions_serializer(response, story):
        directions = map(StorySerializer.format_directions, response['legs'][0]['maneuvers'])
        return list(directions)

    def format_directions(maneuver):
        return {
            'id': None,
            'type': 'directions',
            'attributes': {
                'narrative': maneuver['narrative'],
                'distance': f"{maneuver['distance']} miles",
            }
        }

    def coords_error(request):
        error = {'messages': [], 'code': 0}
        if request == 'Impossible route.':
            error['messages'].append('Impossible route.')
            error['code'] = 2
        elif not Story.coords_present(request):
            error['messages'].append("Latitude or longitude can't be blank.")
            error['code'] = 1
        elif not Story.valid_coords(request):
            error['messages'].append("Invalid latitude or longitude.")
            error['code'] = 1
        return error
