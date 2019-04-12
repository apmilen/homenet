import pytest
from mixer.backend.django import mixer

from rentals import schema

pytestmark = pytest.mark.django_db


def test_rentpropertuy_type():
    instance = schema.RentPropertyType()
    assert instance


def test_resolve_all_rentp():
    for _ in range(5):
        mixer.blend("rentals.RentProperty")

    query = schema.Query()
    res = query.resolve_all_rentp(None)
    assert res.count() == 5


def test_resolve_rentproperty():
    rp = mixer.blend("rentals.RentProperty")
    query = schema.Query()
    res = query.resolve_rentproperty(id=rp.id)
    assert res.id == rp.id

    res2 = query.resolve_rentproperty(id=00)
    assert res2.count() == 0
