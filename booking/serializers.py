from rest_framework import serializers

from .models import Property, Booking, Review


class PropertySerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = "__all__"

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data):
        if "check_in_date" not in data or "check_out_date" not in data:
            raise serializers.ValidationError(
                "Обязательными являются даты как заезда, так и отъезда."
            )
        if data["check_in_date"] >= data["check_out_date"]:
            raise serializers.ValidationError(
                "Дата заезда должна предшествовать дате выезда."
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
