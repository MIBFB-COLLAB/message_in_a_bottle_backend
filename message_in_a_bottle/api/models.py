from django.db import models
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

    def create_dict(story):
        return {
            'key': story['id'],
            'title': story['title'],
            'shapePoints': [
                story['latitude'],
                story['longitude']
            ]
        }
