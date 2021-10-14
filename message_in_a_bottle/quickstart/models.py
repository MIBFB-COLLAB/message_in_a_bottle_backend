from django.db import models

# Create your models here.
class Story(models.Model)
    latitude = models.FloatField()
    longitude = models.FloatField()
    message = models.TextField()
    # optional name of user (can be anonymous)
    name = models.CharField()
