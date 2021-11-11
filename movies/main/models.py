from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя актера')

    def __str__(self):
        return self.name


class Writer(models.Model):
    id = models.TextField(verbose_name='id', primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Имя сценариста')

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.CharField(max_length=255, verbose_name='id', primary_key=True, unique=True)
    title = models.CharField(max_length=255, verbose_name='Название фильма')
    imdb = models.FloatField(verbose_name='Рейтинг фильма', default=0.0)
    genre = models.CharField(max_length=255, verbose_name='Жанры')
    description = models.TextField(verbose_name='Описание фильма')
    writers = models.ManyToManyField(Writer, related_name='Режисеры')
    writers_names = models.TextField(verbose_name='Список имен сценаристов, разделенных запятыми')
    director = models.CharField(max_length=255, verbose_name='Режисер')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры')
    actors_names = models.TextField(verbose_name='Список имен актеров, разделенных запятыми')

    def __str__(self):
        return self.title
