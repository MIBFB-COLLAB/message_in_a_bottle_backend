from django.urls import path
from message_in_a_bottle.api import views

urlpatterns = [
    path('api/', views.story_list),
    path('api/<int:pk>/', views.story_list),
]
