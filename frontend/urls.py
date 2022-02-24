from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("radios/<str:country>", views.radios, name="radios"),
    path("radios", views.radios, name="radios"),
    path("latest", views.latest, name="latestPage"),
    path("favourites", views.favouritePage, name="favouritePage"),
    path("popular/<str:country>", views.popular, name="popular"),
    
    # re_path(r'^radio/(?P<pk>\w+)/(?P<title>[\w ]+)/$', views.radioPage, name="radioPage"),
    path("radio/<str:pk>/<str:title>", views.radioPage, name="radioPage"),
    path("radioplayer/<str:pk>/<str:title>", views.radioPlayerPage, name="radioPlayerPage"),
    path("genre/<str:pk>", views.genrePage, name="genrePage"),
    path("country/<str:pk>", views.countryPage, name="countryPage"),
    path("search", views.search, name="search"),
    path("news/<str:pk>/<str:title>/<str:country>", views.redirect, name="news")

]