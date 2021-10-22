from rest_framework import serializers
from .models import Story

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'latitude', 'longitude', 'message', 'name', 'title', 'location', 'created_at', 'updated_at']

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

    def coordinates_error(self):
        return {
            'coordinates': [
                'Invalid latitude or longitude.'
            ]
        }
