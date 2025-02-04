from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PropertyViewSet, BookingViewSet, ReviewViewSet

router_v1 = DefaultRouter()
router_v1.register("properties", PropertyViewSet)
router_v1.register("bookings", BookingViewSet)
router_v1.register("reviews", ReviewViewSet)
urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
