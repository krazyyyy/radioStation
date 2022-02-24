from django.urls import path

from . import views

urlpatterns = [
    path("getRadios", views.getRadios, name="getRadios"),
    path("getPopularRadios", views.getPopularRadios, name="getPopularRadios"),
    path("getRadios/<str:country>", views.getRadios, name="getRadios"),
    path("getPopularRadios/<str:country>", views.getPopularRadios, name="getPopularRadios"),
    path("allRadios", views.AllRadios, name="allRadios"),
    path("allRadios/<str:country>", views.AllRadios, name="allRadios"),
    path("latest", views.latest, name="latest"),
    path("latest/<str:country>", views.latest, name="latest"),
    path("currentPlaying/<str:pk>", views.getCurrentPlaying, name="currentPlaying"),
    path("recentPlaying/<str:pk>", views.getRecentPlaying, name="recentPlaying"),
    path("getRecents", views.getRecents, name="getRecents"),
    path("getRandomRadio", views.getRandomRadio, name="getRandomRadio"),
    path("getRandomRadio/<str:country>", views.getRandomRadio, name="getRandomRadio"),
    path("getCountries", views.getCountries, name="getCountries"),
    path("getByCategory/<str:pk>", views.getByCategory, name="getByCategory"),
    path("feed", views.getNews, name="feed"),
    path("renderNews/<str:pk>", views.renderNews, name="renderNews"),
    path("renderHomeNews", views.renderHomeNews, name="renderHomeNews"),
    path("renderHomeNews/<str:country>", views.renderHomeNews, name="renderHomeNews"),
    path("renderRadioNews/<str:country>", views.renderRadioNews, name="renderRadioNews"),
    path("getRandomRadios/<str:country>", views.getRandomRadios, name="getRandomRadios"),
    path("getSearches/<str:pk>", views.getSearches, name="getSearches"),
    path("addFavourite/<str:pk>", views.addFavourite, name="addFavourite"),
    path("removeFavourite/<str:pk>", views.removeFavourite, name="removeFavourite"),
    path("FavouriteList", views.FavouriteList, name="FavouriteList"),
]