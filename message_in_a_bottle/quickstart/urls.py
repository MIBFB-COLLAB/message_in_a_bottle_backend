from django.urls import path
from message_in_a_bottle.quickstart import views

urlpatterns = [
    path('quickstart/', views.story_list),
    path('quickstart/<int:pk>/', views.story_list),
]
