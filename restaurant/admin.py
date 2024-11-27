from django.contrib import admin

from .models import Restaurant, Rating,Sales


admin.site.register(Restaurant)
admin.site.register(Rating)
admin.site.register(Sales)
