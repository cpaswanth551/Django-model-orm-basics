from django.urls import path

from . import views

urlpatterns = [
    path("city-list/", views.cityList, name="city_view"),
]
