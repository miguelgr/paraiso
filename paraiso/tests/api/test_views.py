from unittest import mock

import pytest
from rest_framework.test import APIClient, APIRequestFactory

from paraiso.api.views import MovieViewSet
from paraiso.tests.factories import MovieFactory

create_movie_view = MovieViewSet.as_view({"post": "create"})
list_movie_view = MovieViewSet.as_view({"get": "list"})
retrieve_movie_view = MovieViewSet.as_view({"get": "retrieve"})


@pytest.mark.django_db
def test_get_movies_without_search_term():
    factory = APIRequestFactory()
    request = factory.get("/api/v0/movies")
    with mock.patch("paraiso.movies.models.Movie.objects.filter") as filter_movies_mock:
        response = list_movie_view(request)
        assert not filter_movies_mock.called

    assert len(response.data.get("results")) == 0


@pytest.mark.django_db
def test_get_movies_with_search_term_in_db():
    movie = MovieFactory(title="Rambo")
    factory = APIRequestFactory()
    request = factory.get(f"/api/v0/movies?title={movie.title}")
    with mock.patch("paraiso.api.views.get_imdb_movies") as search_movies_mock:
        response = list_movie_view(request)
        assert not search_movies_mock.called

    assert response.data.get("results")[0]["imdb_id"] == movie.imdb_id


@pytest.mark.django_db
def test_get_movies_with_search_term():
    factory = APIRequestFactory()
    request = factory.get(f"/api/v0/movies?title=not_found_movie")
    movie = MovieFactory()
    with mock.patch("paraiso.api.views.get_imdb_movies") as search_movies_mock:
        search_movies_mock.return_value = [movie]
        response = list_movie_view(request)
        assert search_movies_mock.called

    assert response.data.get("results")[0]["imdb_id"] == movie.imdb_id


@pytest.mark.django_db
def test_get_movies_by_id():
    term = "avatar"
    factory = APIRequestFactory()
    movie = MovieFactory(title=term.capitalize())
    request = factory.get(f"/api/v0/movies/{movie.imdb_id}")
    response = retrieve_movie_view(request, imdb_id=movie.imdb_id)
    assert response.data.get("imdb_id") == movie.imdb_id
    assert response.headers.get("x-ipfs-path") == movie.archive_url


@pytest.mark.django_db
def test_post_movie_ko():
    factory = APIRequestFactory()
    request = factory.post("/api/v0/movies", {})
    response = create_movie_view(request)

    assert response.status_code == 400
    assert response.data.get("imdb_id")[0].code == "required"


@pytest.mark.django_db
def test_post_movie_ok():
    factory = APIRequestFactory()
    request = factory.post("/api/v0/movies", {"imdb_id": "tt0123456"})
    response = create_movie_view(request)

    assert response.status_code == 201


@pytest.mark.django_db
def test_post_movie_conflict_existing():
    term = "avatar"
    factory = APIRequestFactory()
    movie = MovieFactory(title=term.capitalize())
    request = factory.post("/api/v0/movies", {"imdb_id": movie.imdb_id})
    response = create_movie_view(request)

    # TODO:fix 409 conflict errors
    assert response.status_code == 400
