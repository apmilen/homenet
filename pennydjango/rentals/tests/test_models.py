from rentals.tests.test_utils import SimpleRentTest
from rentals.models import RentProperty


class RentPropertyTestCase(SimpleRentTest):

    def test_rent_property(self):
        rent_prop = RentProperty.objects.first()
        assert rent_prop.id
        assert rent_prop.contact
        assert rent_prop.address
        assert rent_prop.latitude
        assert rent_prop.longitude
        assert rent_prop.about
        assert rent_prop.bedrooms > 0
        assert rent_prop.baths > 0
        assert rent_prop.pets_allowed
        assert rent_prop.amenities is ""
