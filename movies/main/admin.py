from django.contrib import admin
from .models import Actor, Movie, Writer

admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Writer)