# import pdb
from django.db import models
from django.core.exceptions import ValidationError
# from django.db.models import Model

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

    def clean(self):
        if not -90 <= self.latitude <= 90:
            raise ValidationError(('Latitude is invalid'))
        if not -180 <= long <= 180:
            raise ValidationError(('Longitude is invalid'))

    def create_dict(story):
        return {
            'key': str(story.id),
            'name': story.title,
            'shapePoints': [
                story.latitude,
                story.longitude
            ]
        }

    def map_stories():
        stories = map(Story.create_dict, Story.objects.all())
        return list(stories)

    # def validate_latitude(lat):
    #     return -90 <= lat <= 90
    #
    # def validate_longitude(long):
    #     return -180 <= long <= 180
