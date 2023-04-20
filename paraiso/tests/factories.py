import random

import factory

from django.contrib.auth.models import User

from paraiso.movies.models import Movie


class MovieFactory(factory.django.DjangoModelFactory):
    imdb_id = factory.Sequence(
        lambda n: "tt%s" % "{:07}".format(random.randint(1, 100000))
    )

    class Meta:
        model = Movie


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
