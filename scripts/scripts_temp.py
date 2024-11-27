from django.utils import timezone
from django.db import connection
from django.contrib.auth.models import User

from restaurant.models import Restaurant, Rating


def run():

    restaurant = Restaurant()
    restaurant.name = "Paragan Hotel"
    restaurant.latitude = 54.889
    restaurant.longitude = 89.09
    restaurant.date_opened = timezone.now()
    restaurant.restuarant_type = Restaurant.TypeChoices.INDIAN
    restaurant.save()

    rest_all = Restaurant.objects.all()
    rest_first = Restaurant.objects.first()
    rest_last = Restaurant.objects.last()

    rest_create = Restaurant.objects.create(
        name="Crouching Dragon restaurant",
        latitude=545.889,
        longitude=109.09,
        date_opened=timezone.now(),
        restuarant_type=Restaurant.TypeChoices.CHINESE,
    )

    rating = Rating.objects.first()
    rest = Restaurant.objects.first()

    # print(rest.rating_set.all())  # if no related name is given..

    print(rest.rating.all())

    print(rest.sales.all())

    user = User.objects.first()
    rest = Restaurant.objects.first()

    rating, created = Rating.objects.get_or_create(rating=4, user=user, restaurant=rest)
    print(rating, created)

    # updating the queryset
    rest.update(website="https:abc.com/")

    # print(connection.queries)  # what queries are been run
    print("you are top of the world")
