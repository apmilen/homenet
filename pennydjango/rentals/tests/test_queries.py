from rentals.tests.test_utils import SimpleRentTest

from collections import OrderedDict
from graphene.test import Client
from rentals import queries
from penny.schema import schema


class RentQueriesTestCase(SimpleRentTest):
    def setUp(self):
        super().setUp()
        self.client = Client(schema)

    def test_rentproperty_type(self):
        instance = queries.RentPropertyType()
        assert instance

    def test_resolve_all_rentp(self):
        executed = self.client.execute(
            '''
            query {
              allRentp {
                edges {
                  node {
                    contact
                    publisher {
                      username
                      modelId
                    }
                  }
                }
              }
            }
            '''
        )
        assert not executed.get("errors")
        expected = {
            "allRentp": OrderedDict({
                "edges": [
                    OrderedDict({
                        "node": OrderedDict({
                            "contact": ob.contact,
                            "publisher": OrderedDict({
                                "username": ob.publisher.username,
                                "modelId": str(ob.publisher.model_id)
                            })
                        })
                    })
                    for ob in self.properties
                ]
            })
        }
        assert dict(executed.get("data")) == expected

    def test_resolve_rentproperty(self):
        executed = self.client.execute(
            '''
            query getProper($id: UUID!){
              rentproperty(modelId: $id){
                about
              }
            }
            ''',
            variables={'id': str(self.property1.model_id)}
        )
        assert not executed.get("errors")
        expected = {
            "rentproperty": OrderedDict({
                "about": self.property1.about
            })
        }
        assert dict(executed.get("data")) == expected
