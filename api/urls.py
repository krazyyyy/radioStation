from django.urls import path

from . import views

urlpatterns = [
    path("radios", views.getRadios, name="getRadios"),
    path("currentPlaying/<str:pk>", views.getCurrentPlaying, name="currentPlaying"),
    path("recentPlaying/<str:pk>", views.getRecentPlaying, name="recentPlaying"),
    path("getRecents", views.getRecents, name="getRecents"),
    path("getRandomRadio", views.getRandomRadio, name="getRandomRadio"),
    path("getByCategory/<str:pk>", views.getByCategory, name="getByCategory"),
]