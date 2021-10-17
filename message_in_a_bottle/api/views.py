from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer
# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class StoryList(APIView):
    """
    List all stories, or create a new story.
    """
    def get(self, request, format=None):
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return Response({'data':serializer.data})

    def post(self, request, format=None):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class StoryDetail(APIView):
    """
    Retrieve, update or delete a story instance.
    """
    def get_object(self, pk):
        try:
            return Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        story = self.get_object(pk)
        serializer = StorySerializer(story)
        return Response({'data':serializer.data})

    def put(self, request, pk, format=None):
        story = self.get_object(pk)
        serializer = StorySerializer(story, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data})
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        story = self.get_object(pk)
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
