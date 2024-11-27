from django.utils import timezone
from django.db import connection

from restaurant.models import Restaurant, Rating


def run():

    rest = Restaurant.objects.all()

    

    print("you are top of the world")
   