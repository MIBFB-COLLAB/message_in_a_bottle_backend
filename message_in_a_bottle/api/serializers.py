from rest_framework import serializers
from .models import Story

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'latitude', 'longitude', 'message', 'name', 'title', 'location', 'created_at', 'updated_at']

    def reformat(story):
        return {
            'id': story.id,
            'type': story.__class__.__name__,
            'attributes': {
                'name': story.name,
                'title': story.title,
                'message': story.message,
                'latitude': story.latitude,
                'longitude': story.message,
                'location': story.location,
                'created_at': story.created_at,
                'updated_at': story.updated_at
            }
        }
