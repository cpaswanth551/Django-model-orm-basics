from django.urls import path

from app import views

urlpatterns = [
    path("list/", views.OneListview, name="list_view"),
    path("book/", views.bookView, name="book_view"),
]
