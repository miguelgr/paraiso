from django_distill import distill_path

from django.urls import path

from .views import get_movies, movie_list, movie_detail, get_movie_pages

urlpatterns = [
    distill_path(
        "movies/pages/<int:page>/",
        movie_list,
        name="movie-list",
        distill_func=get_movie_pages,
        distill_status_codes=(200, 404),
    ),
    distill_path(
        "movies/<slug:slug>/",
        movie_detail,
        name="movie-detail",
        distill_func=get_movies,
        distill_status_codes=(200, 404),
    ),
]
