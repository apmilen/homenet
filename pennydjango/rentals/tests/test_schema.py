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
