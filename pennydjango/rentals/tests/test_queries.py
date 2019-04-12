import pytest
from collections import OrderedDict
from mixer.backend.django import mixer
from graphene.test import Client

from rentals import queries
from penny.schema import schema

pytestmark = pytest.mark.django_db


def test_rentpropertuy_type():
    instance = queries.RentPropertyType()
    assert instance


def test_resolve_all_rentp():
    properties = []
    for _ in range(2):
        properties.append(mixer.blend("rentals.RentProperty"))
    client = Client(schema)
    executed = client.execute(
        '''
        query {
          allRentp{
            contact
            publisher {
              username
              id
            }
          }
        }
        '''
    )
    assert not executed.get("errors")
    expected = {
        "allRentp": [
            OrderedDict({
                "contact": ob.contact,
                "publisher": OrderedDict({
                    "username": ob.publisher.username,
                    "id": str(ob.publisher.id)
                })
            })
            for ob in properties
        ]
    }
    assert dict(executed.get("data")) == expected


def test_resolve_rentproperty():
    rp = mixer.blend("rentals.RentProperty")
    client = Client(schema)
    executed = client.execute(
        '''
        query getProper($id: ID){
          rentproperty(id: $id){
            about
          }
        }
        ''',
        variables={'id': rp.id}
    )
    assert not executed.get("errors")
    expected = {
        "rentproperty":  OrderedDict({
            "about": rp.about
        })
    }
    assert dict(executed.get("data")) == expected
