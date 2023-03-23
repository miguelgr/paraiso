from rest_framework import routers
from django.urls import path, include

from paraiso.api.views import MovieViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)

urlpatterns = [
    path(r"", include(router.urls)),
]
