from django.test import TestCase
from django.contrib.auth import get_user_model

from rentals.models import RentProperty


class SimpleRentTest(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username='test_pub',
            password='alalalalong'
        )
        self.property1 = RentProperty.objects.create(
            publisher=self.test_user,
            price=999,
            contact='bob at 018000-marley',
            address='420 love street',
            latitude=40.786317,
            longitude=-73.962212,
            about='no rooftop so you can view the stars at night',
            bedrooms=3,
            baths=2,
        )
        self.property2 = RentProperty.objects.create(
            publisher=self.test_user,
            price=2500,
            latitude=40.776720,
            longitude=-73.972723,
            bedrooms=1,
            baths=1,
        )

        self.properties = [
            self.property1,
            self.property2,
        ]
