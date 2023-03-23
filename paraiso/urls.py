"""paraiso URL Configuration"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from paraiso.movies import urls as archive_urls

urlpatterns = [
    path("", RedirectView.as_view(url=settings.PARAISO_API_V1_URL)),
    path("", include(archive_urls)),
    path("admin/", admin.site.urls),
    # path(f"{settings.PARAISO_API_V1_URL}auth/",
    #      include("rest_framework.urls", namespace="rest_framework")),
    path(
        settings.PARAISO_API_V1_URL, include("paraiso.api.urls", namespace="api")
    ),
]
