from django.db import models

# Create your models here.
class Story(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    # optional name of user (can be anonymous)
    name = models.CharField(max_length=50, default='Anonymous')
    title = models.CharField(max_length=50, default='My Story')
    message = models.TextField(max_length=1000)
    location = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def valid_coords(request_dict):
        if 'latitude' in request_dict and 'longitude' in request_dict:
            if not (-90 <= float(request_dict['latitude']) <= 90) or not (-180 <= float(request_dict['longitude']) <= 180):
                return False
            else:
                return True
        else:
            return False

    def mapquest_data_dict(story):
        return {
            'key': str(story.id),
            'name': story.title,
            'shapePoints': [
                story.latitude,
                story.longitude
            ]
        }

    def map_stories():
        stories = map(Story.mapquest_data_dict, Story.objects.all())
        return list(stories)
