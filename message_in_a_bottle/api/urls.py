from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from message_in_a_bottle.api import views

urlpatterns = [
    path('stories', views.StoryList.as_view()),
    path('stories/<int:pk>', views.StoryDetail.as_view()),
    path('stories/<int:pk>/directions', views.StoryDirections.as_view())
]
