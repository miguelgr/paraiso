from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse

from paraiso.movies.models import Movie

DEFAULT_PAGE_SIZE = 25


def movie_list(request, page):
    movies = Movie.objects.all().values_list("slug", "title", named=True)
    paginator = Paginator(movies, DEFAULT_PAGE_SIZE)
    page_obj = paginator.get_page(page)
    return TemplateResponse(request, "paraiso/movie_list.html", {"page_obj": page_obj})


def movie_detail(request, slug):
    movie = Movie.objects.filter(slug=slug).first()
    # Have an static HTML on IPFS
    # if movie and movie.archive_file:
    #     return HttpResponse(
    #         movie.archive_file.read(),
    #         headers={"x-ipfs-path": movie.archive_file.url},
    #     )

    return (
        TemplateResponse(request, "paraiso/movie_detail.html", {"movie": movie})
        if movie
        else HttpResponseNotFound("Movie not found")
    )


def get_movies():
    for movie in Movie.objects.all().values_list("slug")[:5]:
        yield movie


def get_movie_pages():
    movies_qs = Movie.objects.all().values_list("pk", flat=True).order_by("created_at")
    paged = Paginator(movies_qs, DEFAULT_PAGE_SIZE)
    for page in paged.page_range[:1]:
        yield [page]
