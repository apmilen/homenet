from rentals.tests.test_utils import SimpleRentTest


class RentPropertyTestCase(SimpleRentTest):

    def test_rent_property(self):
        rent_prop = self.property1
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
