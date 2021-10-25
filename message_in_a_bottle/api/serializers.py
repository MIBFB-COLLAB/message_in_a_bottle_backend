from rest_framework import serializers
from .models import Story
from message_in_a_bottle.api.services import MapService

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'latitude', 'longitude', 'message', 'name', 'title', 'location', 'created_at', 'updated_at']

    def reformat(self, story_dict, return_distance=None):
        output_dict = {
            'id': story_dict['id'],
            'type': 'Story',
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

    def reformat_condensed(story_obj, distance):
        return {
            'id': story_obj.id,
            'type': story_obj.__class__.__name__,
            'attributes': {
                'title': story_obj.title,
                'latitude': story_obj.latitude,
                'longitude': story_obj.longitude,
                'distance_in_miles': distance
            }
        }

    def stories_near_user(from_lat, from_long, stories):
        output_list = []
        for s in stories:
            delta_lat = abs(float(from_lat) - s.latitude)
            delta_long = abs(float(from_long) - s.longitude)
            if delta_lat <= 2 and delta_long <= 2:
                distance = MapService.get_distance(from_lat, from_long, s.latitude, s.longitude)
                if distance != 'Impossible route.' and distance <= 25:
                    output_list.append(StorySerializer.reformat_condensed(s, distance))
        return sorted(output_list, key = lambda s: s['attributes']['distance_in_miles'])

    def stories_index(stories, city_state):
        return {
            'input_location': city_state,
            'stories': stories
        }

    def stories_index_serializer(response, city_state):
        stories = map(StorySerializer.reformat_mapquest_response, response)
        dict = {
            'input_location': city_state,
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

    # def blank_coords():
    #     return {
    #         'coordinates': [
    #             "Latitude or longitude can't be blank."
    #         ]
    #     }
