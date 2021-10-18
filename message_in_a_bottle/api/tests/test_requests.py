import pytest
from rest_framework.test import APIClient
from message_in_a_bottle.api.views import StoryList
from message_in_a_bottle.api.serializers import StorySerializer

@pytest.mark.django_db
def test_get_story():
    story = {
        'id': 1,
        'title': 'My Cool Story',
        'message': 'I once saw a really pretty flower.',
        'latitude': 123.456892,
        'longitude': -19.982791
    }

    route = '/api/v1/stories'

    client = APIClient()
    response = client.get(route)

    assert response.status_code == 200
