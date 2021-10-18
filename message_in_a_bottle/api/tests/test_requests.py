import pytest
from rest_framework.test import APIClient
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
def test_get_existing_story():
    story = {
        'title': 'My Cool Story',
        'message': 'I once saw a really pretty flower.',
        'latitude': 123.456892,
        'longitude': -19.982791
    }
    assert Story.objects.count() == 0

    Story.objects.create(
        title=story['title'],
        message=story['message'],
        latitude=story['latitude'],
        longitude=story['longitude']
    )
    assert Story.objects.count() == 1

    id = Story.objects.latest('id').id
    route = f'/api/v1/stories/{id}'

    client = APIClient()
    response = client.get(route)
    serializer = StorySerializer(Story.objects.get(pk=id))

    assert response.status_code == 200
    assert response.data['data'] == serializer.data

@pytest.mark.django_db
def test_get_non_existent_story():
    story = {
        'title': 'My Cool Story',
        'message': 'I once saw a really pretty flower.',
        'latitude': 123.456892,
        'longitude': -19.982791
    }

    Story.objects.create(
        title=story['title'],
        message=story['message'],
        latitude=story['latitude'],
        longitude=story['longitude']
    )

    id = Story.objects.latest('id').id + 1
    route = f'/api/v1/stories/{id}'

    client = APIClient()
    response = client.get(route)

    assert response.status_code == 404
