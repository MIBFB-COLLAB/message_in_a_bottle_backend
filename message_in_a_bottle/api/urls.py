from django.urls import path
from message_in_a_bottle.api import views

urlpatterns = [
    path('api/v1/stories/', views.story_list),
    path('api/v1/stories/<int:pk>/', views.story_detail),
]
