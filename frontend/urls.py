from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("radio/<str:pk>", views.radioPage, name="radioPage")
]