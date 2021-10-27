from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer
from message_in_a_bottle.api.services import MapService
from message_in_a_bottle.api.facades import MapFacade
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StoryList(APIView):
    def errors_response(self, error):
        return Response({'errors':StorySerializer.coords_error(error)}, status=status.HTTP_400_BAD_REQUEST)
    """
    List all stories.
    """
    def get(self, request, format=None):
        if StorySerializer.coords_error(request.query_params)['code'] == 1:
            return self.errors_response(request.query_params)
        else:
            results = MapFacade.get_stories(request.query_params)
            serializer = StorySerializer.stories_index(*results)
            return Response({'data':serializer}, status=status.HTTP_200_OK)

    """
    Create a story.
    """
    def post(self, request, format=None):
        if StorySerializer.coords_error(request.data)['code'] == 1:
            return self.errors_response(request.data)
        else:
            request.data['location'] = MapFacade.get_city_state(request.data)
            serializer = StorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.reformat(serializer.data)}, status=status.HTTP_201_CREATED)
            return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class StoryDetail(APIView):
    def errors_response(self, error):
        return Response({'errors':StorySerializer.coords_error(error)}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            raise Http404
    """
    Retrieve a story instance.
    """
    def get(self, request, pk, format=None):
        if StorySerializer.coords_error(request.query_params)['code'] not in [1, 2]:
            story = self.get_object(pk)
            distance = MapFacade.get_distance(request.query_params, story)
            if distance == 'Impossible route.':
                return self.errors_response(distance)
            else:
                serializer = StorySerializer(story)
                return Response({'data':serializer.reformat(serializer.data, return_distance=distance)})
        return self.errors_response(request.query_params)

    """
    Update a story instance.
    """
    def patch(self, request, pk, format=None):
        story = self.get_object(pk)
        serializer = StorySerializer(story, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.reformat(serializer.data)})
        return self.errors_response(serializer.errors)
    """
    Delete a story instance.
    """
    def delete(self, request, pk, format=None):
        story = self.get_object(pk)
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StoryDirections(APIView):
    def errors_response(self, error):
        return Response({'errors':StorySerializer.coords_error(error)}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            raise Http404
    """
    Get directions to a story.
    """
    def get(self, request, pk, format = None):
        if StorySerializer.coords_error(request.query_params)['code'] not in [1, 2]:
            story = self.get_object(pk)
            response = MapFacade.get_directions(request.query_params, story)
            if response == 'Impossible route.':
                return self.errors_response(response)
            return Response({'data':StorySerializer.story_directions(response, story)})
        return self.errors_response(request.query_params)
