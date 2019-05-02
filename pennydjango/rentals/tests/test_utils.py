# from penny.tests.test_utils import GraphClientTestCase
from django.test import TestCase

from penny.models import User
from rentals.models import RentProperty


class SimpleRentTest(TestCase):
    def setUp(self):
        super().setUp()
        self.test_user = User.objects.create_user(
            email='test@test.com',
            username='test_pub',
            password='alalalalong'
        )
        self.property1 = RentProperty.objects.create(
            publisher=self.test_user,
            price=999,
            contact='bob at 018000-marley',
            address='420 love street',
            geopoint="POINT (-73.92617910000001 40.7106363)",
            about='no rooftop so you can view the stars at night',
            bedrooms=3,
            baths=2,
        )
        self.property2 = RentProperty.objects.create(
            publisher=self.test_user,
            price=2500,
            bedrooms=1,
            baths=1,
            geopoint="POINT (-73.92617910000001 40.7106363)",
        )

        self.properties = [
            self.property1,
            self.property2,
        ]

    def tearDown(self):
        super().tearDown()
        self.test_user.delete()
        self.property1.delete()
        self.property2.delete()
