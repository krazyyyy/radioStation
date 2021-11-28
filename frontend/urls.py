from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("radio/<str:pk>", views.radioPage, name="radioPage"),
    path("radioplayer/<str:pk>", views.radioPlayerPage, name="radioPlayerPage"),
    path("genre/<str:pk>", views.genrePage, name="genrePage")
]