import re
import uuid

from django.db import IntegrityError, models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from paraiso.search import get_imdb_movies

# from ipfs_storage.storage import InterPlanetaryFileSystemStorage


def validate_imdb_id(_id: str):
    "Validates a pattern for an IMDB movie id, like: tt0120338"
    if not _id:
        raise ValidationError("Invalid IMDB id: empty")

    imdb_id_pattern = r"tt[0-9]{7,8}"
    matches = re.match(imdb_id_pattern, _id)

    if not matches:
        raise ValidationError("Invalid IMDB id: format")


class MovieManager(models.Manager):
    def get_imdb_suggestions(self, term):
        return [
            Movie(
                title=movie.get("l"),
                year=movie.get("y"),
                imdb_id=movie.get("id"),
                image=movie.get("i", {}).get("imageUrl"),
            )
            for movie in get_imdb_movies(term)
        ]

    def create_from_imdb(self, imdb_id):
        self.validate_external_id(imdb_id)
        data = {}
        try:
            imdb_data = get_imdb_movies(imdb_id)[0]
            data["imdb_id"] = imdb_id
            data["title"] = imdb_data.get("l")
            data["year"] = imdb_data.get("y")
            data["image"] = imdb_data.get("i", {}).get("imageUrl")
        except (AttributeError, IndexError):
            raise ValidationError("Invalid IMDB movie id")
        return super().create(**data)

    def validate_external_id(self, _id):
        validate_imdb_id(_id)
        if self.filter(imdb_id=_id).exists():
            raise IntegrityError("Existing movie with given IMDB id")


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imdb_id = models.CharField(unique=True, null=True, max_length=9, editable=False)
    cid = models.CharField(unique=True, null=True, max_length=46)

    title = models.CharField(verbose_name=_("Title"), max_length=128)
    slug = models.CharField(
        verbose_name=_("Slug"), max_length=128, unique=True, editable=False
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    image = models.URLField(verbose_name=_("Video Poster"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    # # IPFS content
    # archive_file = models.FileField(
    #     storage=InterPlanetaryFileSystemStorage(),
    #     null=True,
    #     blank=True
    # )

    objects = MovieManager()

    def __str__(self):
        return f"{self.title}"

    @property
    def search_term(self):
        return "{selt.title} {self.year}"

    @property
    def archive_url(self):
        return f"{settings.IPFS_STORAGE_GATEWAY_API_URL}/{self.cid}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
