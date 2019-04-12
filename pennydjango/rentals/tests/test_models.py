from django.test import TestCase
from django.contrib.auth import get_user_model

from rentals.models import RentProperty


class RentPropertyTestCase(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username='test_pub',
            password='alalalalong'
        )
        RentProperty.objects.create(
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

    def test_rent_property(self):
        rent_prop = RentProperty.objects.get(publisher=self.test_user)
        assert rent_prop.id
        assert rent_prop.contact
        assert rent_prop.address
        assert rent_prop.latitude
        assert rent_prop.longitude
        assert rent_prop.about
        assert rent_prop.bedrooms == 3
        assert rent_prop.baths == 2
        assert rent_prop.pets_allowed
        assert rent_prop.amenities is ""
