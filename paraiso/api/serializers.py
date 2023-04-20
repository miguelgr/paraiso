from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from paraiso.movies.models import Movie, validate_imdb_id

MOVIE_PUBLIC_FIELDS = (
    "title",
    "description",
    "year",
    "image",
    "imdb_id",
    "cid",
    "archive_url",
)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = MOVIE_PUBLIC_FIELDS
        read_only_fields = MOVIE_PUBLIC_FIELDS


class CreateMovieSerializer(serializers.Serializer):
    imdb_id = serializers.CharField(
        min_length=9,
        max_length=10,
        required=True,
        validators=[UniqueValidator(queryset=Movie.objects.all()), validate_imdb_id],
    )

    def save(self):
        try:
            return Movie.objects.create_from_imdb(self.validated_data["imdb_id"])
        except:
            raise serializers.ValidationError("Error processing request", code=422)
