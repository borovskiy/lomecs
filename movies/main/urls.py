from django.urls import path
from .views import GenreApi, ActorsApi, DirectorsApi

urlpatterns = [
    path('genres/', GenreApi.as_view(), name='genre'),
    path('actors/', ActorsApi.as_view(), name='actors'),
    path('directors/', DirectorsApi.as_view(), name='directors')
]
