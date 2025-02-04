from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register("users", UserViewSet)

urlpatterns = [
    path("v1/users/", include(router_v1.urls)),
]
