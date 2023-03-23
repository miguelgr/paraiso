import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    imdb_id = models.CharField(unique=True, null=True, max_length=128)
    cid = models.CharField(unique=True, null=True, max_length=46)

    title = models.CharField(verbose_name=_("Title"), max_length=128)
    slug = models.CharField(verbose_name=_("Slug"), max_length=128, unique=True)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    image = models.URLField(verbose_name=_("Video Poster"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
