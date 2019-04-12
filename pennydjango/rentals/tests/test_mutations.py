import json
import pytest
from mixer.backend.django import mixer

from decimal import Decimal

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from graphene.test import Client

from rentals import mutations
from penny.schema import schema


pytestmark = pytest.mark.django_db


def test_create_rentproperty_mutation():
    user = mixer.blend("penny.User")
    data = {
        "price": 2500,
        "contact": "me",
        "address": "my lil house",
        "latitude": 3.074567,
        "longitude": -76.5677,
        "about": "this is a nice house, don't u think? ;)",
        "bedrooms": 3,
        "baths": 2,
        "amenities": "a lot"
    }
    req = RequestFactory().get('/')
    req.user = AnonymousUser()
    client = Client(schema)
    executed = client.execute(
        '''
        mutation createRentP($input: RentPropertyInput!) {
          createRentproperty(rentp: $input) {
            status
            formErrors
          }
        }
        ''',
        variables={"input": data},
        context=req
    )
    assert not executed.get("errors")
    res = executed["data"]["createRentproperty"]
    assert res["status"] == 403, "user not authenticated"

    # req.user = user
    # res = mutation.mutate(None, {}, req, None)
    # assert res.status == 400, 'Should return 400 if there are form errors'
    # assert "message" in res.formErrors, "should have form error field"
    #
    # req.user = user
    # res = mutation.mutate(None, data, req, None)
    # assert res.status == 200, "should return 200 if mutation is successful"
    # assert res.rent_property.id
