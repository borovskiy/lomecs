from django.db.models import Count, Avg
from rest_framework import status, response, views
from .models import Movie, Actor
from .serializers import GenreSerializer, ActorSerializer, DirectorSerializer


class GenreApi(views.APIView):
    def get(self, request):
        queryset = Movie.objects.all().values('genre').annotate(movies_count=Count('genre'), avg_rating=Avg('imdb'))
        serializer = GenreSerializer(instance=queryset, many=True)
        return response.Response(serializer.data, status.HTTP_200_OK)


class ActorsApi(views.APIView):

    def get(self, request):
        ## Просто наглядный пример как можно использовать чистый SQL для запроса в DRF
        select = """
        SELECT *, COUNT(name) as movies_count, MAX(imdb) as max_imdb FROM main_actor 
        LEFT JOIN main_movie_actors ON main_actor.id=main_movie_actors.actor_id
        LEFT JOIN main_movie ON main_movie_actors.movie_id=main_movie.id
        GROUP BY name ORDER BY main_actor.id"""

        queryset = Actor.objects.raw(select)
        serializer = ActorSerializer(instance=queryset, many=True)
        return response.Response(serializer.data, status.HTTP_200_OK)


class DirectorsApi(views.APIView):

    def get(self, request):
        queryset = Movie.objects.all().values('director').annotate(count=Count('director'))[:20]
        serializer = DirectorSerializer(instance=queryset, many=True)
        return response.Response(serializer.data, status.HTTP_200_OK)
