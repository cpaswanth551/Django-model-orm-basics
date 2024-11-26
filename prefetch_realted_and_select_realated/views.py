from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from prefetch_realted_and_select_realated.models import City, Province, Person


def cityList(request):
    cities = City.objects.select_related().all()

    # cities in a Province => 'malabar'
    hb = Province.objects.prefetch_related("city_set").get(name__iexact="malabar")

    #  cities visited by a person  => 'Nithish'
    person_visted = Person.objects.prefetch_related("visitation").get(
        firstname__iexact="Nithish"
    )
    # people visited a city => 'Tirur'
    city_visited = City.objects.prefetch_related("visitor").get(name__iexact="tirur")

    #  city where a particular person lives
    city_living_in = Person.objects.select_related("living").all()

    # count the number of people living in each city
    city_living_count = City.objects.annotate(residents_count=Count("citizen"))

    for city in city_living_count:
        print(f"{city.name}: {city.residents_count} residents")

    return HttpResponse("hello")
