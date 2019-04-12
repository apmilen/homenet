import pytest

from mixer.backend.django import mixer


# We need to do this so that writing to the DB is possible in our tests.
pytestmark = pytest.mark.django_db


def test_rent_property():
    rent_prop = mixer.blend('rentals.RentProperty')
    assert rent_prop.id
    assert rent_prop.contact
    assert rent_prop.address
    assert rent_prop.latitude
    assert rent_prop.longitude
    assert rent_prop.about is None
    assert rent_prop.bedrooms
    assert rent_prop.baths
    assert rent_prop.pets_allowed
    assert rent_prop.amenities
