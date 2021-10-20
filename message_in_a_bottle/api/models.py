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

    def valid_coords(story):
        if 'latitude' in story and 'longitude' in story:
            if not -90 <= story['latitude'] <= 90:
                return False
            elif not -180 <= story['longitude'] <= 180:
                return False
            else:
                return True
        else:
            return False

    def create_dict(story):
        return {
            'key': story.id,
            'title': story.title,
            'shapePoints': [
                story.latitude,
                story.longitude
            ]
        }

    def map_stories():
        stories = map(Story.create_dict, Story.objects.all())
        return list(stories)
