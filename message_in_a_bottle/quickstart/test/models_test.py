from message_in_a_bottle.quickstart.models import Story

def test_create_dict():
    story = {
        "id": 1,
        "title": 'My Cool Story',
        "message": 'I once saw a really pretty flower.',
        "latitude": 123.456892,
        "longitude": -19.982791
    }

    assert Story.create_dict(story) == {
        "key": 1,
        "title": 'My Cool Story',
        "shapePoints": [
            123.456892, -19.982791
        ]
    }
