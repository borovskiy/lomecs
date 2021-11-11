from django.db.models import Count
from rest_framework import serializers

from .models import Movie, Actor


class GenreSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField()
    avg_rating = serializers.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        model = Movie
        fields = ['genre', 'movies_count', 'avg_rating']


class ActorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField()
    genre = serializers.CharField()

    class Meta:
        model = Actor
        fields = ['name', 'movies_count', 'genre']

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('field', None)
        super(ActorSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)


class FilmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'imdb']


class DirectorSerializer(serializers.ModelSerializer):
    favourite_actors = serializers.SerializerMethodField('get_list')
    best_movies = serializers.SerializerMethodField('get_movies')

    class Meta:
        model = Movie
        fields = ['director', 'favourite_actors', 'best_movies']

    @classmethod
    def get_list(cls, instance):
        actors = Actor.objects.filter(movie__director=instance['director']).annotate(
            movies_count=Count('name')).distinct().order_by('-movies_count')[:3]
        return ActorSerializer(actors, many=True, field=['genre']).data

    @classmethod
    def get_movies(cls, instance):
        movies = Movie.objects.filter(director=instance['director']).values('title', 'imdb').order_by('-imdb')[:3]
        serializer = FilmsSerializer(movies, many=True)
        return serializer.data
