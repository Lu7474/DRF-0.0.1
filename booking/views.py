from datetime import date
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Property, Booking, Review
from .permissions import IsOwnerOrReadOnly
from .serializers import PropertySerializer, BookingSerializer, ReviewSerializer


class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start_date",
                location=OpenApiParameter.QUERY,
                description="Start_date",
                required=True,
                type=date,
            ),
            OpenApiParameter(
                name="end_date",
                location=OpenApiParameter.QUERY,
                description="End_date",
                required=True,
                type=date,
            ),
        ]
    )
    @action(detail=True, methods=["get"])
    def availability(self, request, pk=True):
        property = self.get_object()
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Требуются значения start_date и end_date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_availability = not Booking.objects.filter(
            property=property,
            check_in_date=start_date,
            check_out_date=end_date,
            status="confirmed",
        ).exists()

        return Response({"is_availability": is_availability})


# создания, просмотра, обновления и удаления объявлений


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# бронирования жилья, отмены и просмотра бронирований.


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# добавления, редактирования и просмотра отзывов.
