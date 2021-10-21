from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer
from message_in_a_bottle.api.services import MapService
# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

class StoryList(APIView):
    """
    List all stories.
    """
    def get(self, request, format=None):
        if Story.valid_user_coords(request.query_params):
            stories = Story.map_stories()
            response = MapService.get_stories(float(request.query_params['lat']), float(request.query_params['long']), stories)
            if response['resultsCount'] == 0:
                serializer = StorySerializer.stories_index_serializer([])
            else:
                serializer = StorySerializer.stories_index_serializer(response['searchResults'])
            return Response({'data':serializer}, status=status.HTTP_200_OK)
        else:
            error = 'Invalid latitude and longitude'
            return Response({'errors':error}, status=status.HTTP_400_BAD_REQUEST)
    """
    Create a story.
    """
    def post(self, request, format=None):
        story = Story.objects.create(title = request.data['title'], message = request.data['message'], latitude = request.data['latitude'], longitude = request.data['longitude'], location = request.data['location'])
        try:
            story.full_clean()
        except ValidationError:
            story.delete()
            error = "Latitude or Longitude is invalid"
            return Response({'errors':error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = StorySerializer(data=request.data)
            if serializer.is_valid():
                return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)


class StoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            raise Http404

    """
    Retrieve a story instance.
    """
    def get(self, request, pk, format=None):
        story = self.get_object(pk)
        serializer = StorySerializer(story)
        return Response({'data':serializer.data})

    """
    Update a story instance.
    """
    def put(self, request, pk, format=None):
        story = self.get_object(pk)
        serializer = StorySerializer(story, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data})
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    """
    Delete a story instance.
    """
    def delete(self, request, pk, format=None):
        story = self.get_object(pk)
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
