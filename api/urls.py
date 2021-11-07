from django.urls import path

from . import views

urlpatterns = [
    path("radios", views.getRadios, name="getRadios"),
    path("currentPlaying/<str:pk>", views.getCurrentPlaying, name="currentPlaying"),
    path("recentPlaying/<str:pk>", views.getRecentPlaying, name="recentPlaying")
]