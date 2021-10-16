# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.serializers import StorySerializer

# Create your views here.
# TODO: remove @csrf_exempt line after testing / troubleshooting complete
@csrf_exempt
def story_list(request):
    """
    List all stories, or create a new story.
    """
    if request.method == 'GET':
        stories = Story.objects.all()
        serializer = StorySerializer(stories, many=True)
        return JsonResponse({'data': serializer.data}, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=201)
        return JsonResponse({'errors': serializer.errors}, status=400)

# TODO: remove @csrf_exempt line after testing / troubleshooting complete
@csrf_exempt
def story_detail(request, pk):
    """
    Retrieve, update or delete a story.
    """
    try:
        story = Story.objects.get(pk=pk)
    except Story.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StorySerializer(story)
        return JsonResponse({'data': serializer.data})
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StorySerializer(story, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data})
        return JsonResponse({'errors': serializer.errors}, status=400)
    elif request.method == 'DELETE':
        story.delete()
        return HttpResponse(status=204)
