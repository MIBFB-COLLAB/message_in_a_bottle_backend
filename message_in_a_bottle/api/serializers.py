from rest_framework import serializers
from .models import Story
from message_in_a_bottle.api.services import MapService

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'latitude', 'longitude', 'message', 'name', 'title', 'location', 'created_at', 'updated_at']

    def reformat(self, story, return_distance=None):
        output_dict = {
            'id': story['id'],
            'type': 'Story',
            'attributes': {
                'name': story['name'],
                'title': story['title'],
                'message': story['message'],
                'latitude': story['latitude'],
                'longitude': story['longitude'],
                'location': story['location'],
                'created_at': story['created_at'],
                'updated_at': story['updated_at']
            }
        }
        if return_distance is not None:
            output_dict['attributes']['distance_in_miles'] = return_distance
        return output_dict

    def stories_near_user(from_lat, from_long, stories):
        output_list = []
        for s in stories:
            distance = MapService.get_distance(from_lat, from_long, s.latitude, s.longitude)
            if distance != 'Impossible route.' and distance <= 25:
                output_list.append({
                    'id': s.id,
                    'type': s.__class__.__name__,
                    'attributes': {
                        'title': s.title,
                        'latitude': s.latitude,
                        'longitude': s.longitude,
                        'distance_in_miles': distance
                    }
                })
        return sorted(output_list, key = lambda s: s['attributes']['distance_in_miles'])

    def stories_index(city_state, stories):
        return {
            'input_location': city_state,
            'stories': stories
        }

    def stories_index_serializer(response):
        stories = map(StorySerializer.reformat_mapquest_response, response)
        dict = {
            'input_location': 'This is a temporary location!',
            'stories': list(stories)
        }
        return dict

    def reformat_mapquest_response(story):
        if story:
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

    def coords_error(response=None):
        if response is None:
            return {'coordinates': ['Invalid latitude or longitude.']}
        elif response == 'Impossible route.' or response['routeError']['errorCode'] == 2:
            return {'message': ['Impossible route.']}

    def blank_coords():
        return {
            'coordinates': [
                "Latitude or longitude can't be blank."
            ]
        }
