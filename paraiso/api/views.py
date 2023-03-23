import django_filters.rest_framework
from rest_framework import viewsets

from paraiso.movies.models import (
    Movie
)
from paraiso.api.serializers import *


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
