import re

import django_filters.rest_framework
from rest_framework import status, viewsets
from rest_framework.response import Response

from django.core.exceptions import ValidationError

from paraiso.movies.models import Movie
from paraiso.api.serializers import *


class MovieViewSet(viewsets.ModelViewSet):
    lookup_field = "imdb_id"
    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieSerializer
    allowed_http_methods = ["head", "get", "post"]

    def get_queryset(self):
        title = self.request.query_params.get("title")
        imdb_id = self.kwargs.get("imdb_id")

        if not title and not imdb_id:
            return Movie.objects.none()

        if not title and imdb_id:
            return Movie.objects.filter(imdb_id=imdb_id)

        qs = Movie.objects.filter(title__contains=title)
        if qs.count() > 0:
            return qs

        return Movie.objects.get_imdb_suggestions(term=title)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.headers["x-ipfs-path"] = f"{response.data['archive_url']}"
        return response

    def create(self, request, *args, **kwargs):
        serializer = CreateMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()
        headers = {"x-ipfs-path": movie.archive_url}
        return Response(
            MovieSerializer(instance=movie).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
