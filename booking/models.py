from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()

class Property(models.Model):
    PROPERTY_TYPES = (
        ("hotel", "Отель"),
        ("apartment", "Апартаменты"),
        ("house", "Дом"),
        ("villa", "Вилла"),
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField()  # validators=[MaxValueValidator(1)]
    bedrooms = models.IntegerField()  # validators=[MinValueValidator(0)]
    bathrooms = models.IntegerField()  # validators=[MinValueValidator(0)]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Ожидает подтверждения"),
        ("confirmed", "Подтверждено"),
        ("cancelled", "Отменено"),
        ("completed", "Завершено"),
    )
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests_count = models.IntegerField()  # validators=[MinValueValidator(0)]
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
