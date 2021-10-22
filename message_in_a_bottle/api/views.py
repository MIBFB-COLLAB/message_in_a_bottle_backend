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
        coords_check = Story.valid_coords(request.data)
        if coords_check:
            serializer = StorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.reformat(serializer.data)}, status=status.HTTP_201_CREATED)
            return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {'coordinates': ['Invalid latitude or longitude.']}
            return Response({'errors':error}, status=status.HTTP_400_BAD_REQUEST)


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

class StoryDirections(APIView):
    def get_object(self, pk):
        try:
            return Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        if Story.valid_coords(request.query_params):
            story = self.get_object(pk)
            response = MapService.get_directions(request.query_params, story)['route']
            serializer = StorySerializer.story_directions_serializer(response, story)
            return Response({'data':serializer}, status=status.HTTP_200_OK)
        else:
            error = 'Invalid latitude and longitude'
            return Response({'errors':error}, status=status.HTTP_400_BAD_REQUEST)
