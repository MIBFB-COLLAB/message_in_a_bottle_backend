from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer
from message_in_a_bottle.api.services import MapService
from message_in_a_bottle.api.facades import MapFacade
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StoryList(APIView):
    """
    List all stories.
    """
    def get(self, request, format=None):
        coords_present = Story.coords_present(request.query_params)
        coords_check = Story.valid_coords(request.query_params) if coords_present else False
        if coords_present and coords_check:
            input_lat = request.query_params['latitude']
            input_long = request.query_params['longitude']
            results = MapFacade.get_stories(input_lat, input_long)
            serializer = StorySerializer.stories_index_serializer(*results)
            return Response({'data':serializer}, status=status.HTTP_200_OK)
        else:
            error = StorySerializer.coords_error() if coords_present and not coords_check else StorySerializer.blank_coords()
            return Response({'errors':error}, status=status.HTTP_400_BAD_REQUEST)
    """
    Create a story.
    """
    def post(self, request, format=None):
        coords_check = Story.valid_coords(request.data)
        if coords_check:
            request.data['location'] = MapFacade.get_city_state(request)
            serializer = StorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.reformat(serializer.data)}, status=status.HTTP_201_CREATED)
            return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors':StorySerializer.coords_error()}, status=status.HTTP_400_BAD_REQUEST)

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
        coords_present = Story.coords_present(request.query_params)
        coords_check = Story.valid_coords(request.query_params) if coords_present else False
        if coords_present and coords_check:
            distance = MapFacade.get_distance(request, story)
        else:
            distance = None
            error = StorySerializer.coords_error() if coords_present and not coords_check else StorySerializer.blank_coords()
            return Response({'errors':error}, status=status.HTTP_400_BAD_REQUEST)
        if distance is not None and distance != 'Impossible route.':
            serializer = StorySerializer(story)
            return Response({'data':serializer.reformat(serializer.data, return_distance=distance)})
        else:
            return Response({'errors':StorySerializer.coords_error(distance)}, status=status.HTTP_400_BAD_REQUEST)
    """
    Update a story instance.
    """
    def patch(self, request, pk, format=None):
        story = self.get_object(pk)
        serializer = StorySerializer(story, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.reformat(serializer.data)})
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
        else:
            response = None
        if response is not None and response['routeError']['errorCode'] != 2:
            serializer = StorySerializer.story_directions_serializer(response, story)
            return Response({'data':serializer}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':StorySerializer.coords_error(response)}, status=status.HTTP_400_BAD_REQUEST)
