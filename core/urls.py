

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app.urls")),
    path("api/books/", include("aggregatevsannotate.urls")),
    path("api/city/", include("prefetch_realted_and_select_realated.urls")),
]
