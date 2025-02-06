from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from booking.models import Property, Booking, Review
from datetime import date

User = get_user_model()


class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.property = Property.objects.create(
            name="Test Property",
            description="Nice place",
            property_type="apartment",
            address="123 Street",
            city="Test City",
            country="Test Country",
            owner=self.user,
            price_per_night=100.0,
            max_guests=4,
            bedrooms=2,
            bathrooms=1,
        )

        self.booking = Booking.objects.create(
            property=self.property,
            user=self.user,
            check_in_date=date.today(),
            check_out_date=date.today(),
            guests_count=2,
            total_price=200.0,
            status="pending",
        )

        self.review = Review.objects.create(
            property=self.property, user=self.user, rating=5, comment="Great place!"
        )

    # ---------- Property Tests ----------
    def test_create_property(self):
        data = {
            "name": "New Property",
            "description": "A new test property",
            "property_type": "house",
            "address": "456 New Street",
            "city": "New City",
            "country": "New Country",
            "owner": self.user.id,
            "price_per_night": 150.0,
            "max_guests": 5,
            "bedrooms": 3,
            "bathrooms": 2,
        }
        response = self.client.post("/api/v1/properties/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_property_list(self):
        response = self.client.get("/api/v1/properties/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_property_detail(self):
        response = self.client.get(f"/api/v1/properties/{self.property.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_property(self):
        data = {"name": "Updated Property"}
        response = self.client.patch(f"/api/v1/properties/{self.property.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.property.refresh_from_db()
        self.assertEqual(self.property.name, "Updated Property")

    def test_delete_property(self):
        response = self.client.delete(f"/api/v1/properties/{self.property.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_check_availability(self):
        response = self.client.get(
            f"/api/v1/properties/{self.property.id}/availability/",
            {"start_date": "2025-02-01", "end_date": "2025-02-10"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_availability", response.data)

    # ---------- Booking Tests ----------
    def test_create_booking(self):
        data = {
            "property": self.property.id,
            "user": self.user.id,
            "check_in_date": "2025-03-01",
            "check_out_date": "2025-03-05",
            "guests_count": 3,
            "total_price": 500.0,
            "status": "pending",
        }
        response = self.client.post("/api/v1/bookings/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_booking_list(self):
        response = self.client.get("/api/v1/bookings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_booking_detail(self):
        response = self.client.get(f"/api/v1/bookings/{self.booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_booking(self):
        data = {"status": "confirmed"}
        response = self.client.patch(f"/api/v1/bookings/{self.booking.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")

    def test_delete_booking(self):
        response = self.client.delete(f"/api/v1/bookings/{self.booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------- Review Tests ----------
    def test_create_review(self):
        data = {
            "property": self.property.id,
            "user": self.user.id,
            "rating": 4,
            "comment": "Nice stay",
        }
        response = self.client.post("/api/v1/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_review_list(self):
        response = self.client.get("/api/v1/reviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_review_detail(self):
        response = self.client.get(f"/api/v1/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        data = {"rating": 3}
        response = self.client.patch(f"/api/v1/reviews/{self.review.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)

    def test_delete_review(self):
        response = self.client.delete(f"/api/v1/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
