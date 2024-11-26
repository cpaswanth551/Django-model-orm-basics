from django.urls import path

from . import views

urlpatterns = [
    path("book-list/", views.bookView, name="book_view"),
]
