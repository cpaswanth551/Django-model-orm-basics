import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, Avg, Sum, Max
from .models import Author, Book, OneModel
from django.db.models import Count

from django.http import HttpResponse
from django.db.models import Avg, Sum, Max, Q
from .models import OneModel


def OneListview(request):
    """
    A view that demonstrates various ORM query concepts using the OneModel.
    It includes examples of basic filtering, chaining filters with exclude,
    using aggregate functions, and annotating query results.
    """

    one_list = OneModel.objects.all()

    one_filter_by_title = OneModel.objects.filter(title="hello users")

    one_filter_has_same_title_and_description_with_given_command = (
        OneModel.objects.filter(Q(age__gte=20) & Q(title__startswith="h"))
    ).values()

    one_filter_with_exclude = (
        OneModel.objects.filter(title__startswith="h").exclude(age__gte=25).values()
    )

    one_filter_aggregate = (
        OneModel.objects.all()
        .aggregate(avg_age=Avg("age"), sum_age=Sum("age"), max_age=Max("age"))
        .values()
    )

    one_filter_annotate = OneModel.objects.annotate(avg_age=Avg("age")).values()

    one_filter_list = OneModel.objects.all()
    one_map = {one.pk: {one.title, one.description} for one in one_filter_list}

    return HttpResponse("hello")


def bookView(request):
    books_with_author_selectrelated = (
        Book.objects.filter(owner__name="Aswanth C P")
        .select_related("owner")
        .only("id", "name", "owner__name")
    )

    author__published_book_year = (
        Author.objects.prefetch_related("book_author")
        .filter(book_author__published_date__year=2024)
        .distinct()
    )

    authors_with_book_count = Author.objects.annotate(
        book_count=Count("book_author")
    ).prefetch_related("book_author")

    books = Book.objects.raw("select * from app_book where name like 'b%'")
    for book in books:
        print(book.name)

    return HttpResponse("hello")
