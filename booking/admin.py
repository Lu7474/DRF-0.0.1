from django.contrib import admin

from .models import Property, Review, Booking

admin.site.register(Property)
admin.site.register(Review)
admin.site.register(Booking)
