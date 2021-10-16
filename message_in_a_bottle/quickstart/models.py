from django.db import models
# from django.db.models import Model

# Create your models here.
class Story(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    message = models.TextField()
    # optional name of user (can be anonymous)
    name = models.CharField(max_length=50, default='Anonymous')
    title = models.CharField(max_length=50, default='My Story')
    location = models.CharField(max_length=50, default='')

    def create_dict(story):
        return {
            "key": story.id,
            "title": story.title,
            "shapePoints": [
                story.latitude,
                story.longitude
            ]
        }