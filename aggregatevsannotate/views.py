from django.http import HttpResponse
from django.db.models import Count, Avg, Sum

from .models import *


def bookView(request):
    """
    Use aggregate() for calculating summary values across the entire queryset.
    Use annotate() for adding calculated fields to each record in the queryset.

    """
    summary = Author.objects.aggregate(
        total_books=Count("book"), avg_books=Avg("book"), sum_books=Sum("book")
    )
    print(summary)

    author_summary = Author.objects.annotate(
        total_books=Count("book"), avg_books=Avg("book")
    )
    for author in author_summary:
        print(
            f"{author.name} - Total Books: {author.total_books}, Avg Books: {author.avg_books}"
        )

    return HttpResponse("hello")
