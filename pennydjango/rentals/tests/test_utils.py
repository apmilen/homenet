from rentals.models import RentProperty
from penny.tests.test_utils import GraphClientTestCase


class SimpleRentTest(GraphClientTestCase):
    def setUp(self):
        super().setUp()
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

    def tearDown(self):
        super().tearDown()
        self.property1.delete()
        self.property2.delete()
