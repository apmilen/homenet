from collections import OrderedDict

from rentals import queries
from rentals.tests.test_utils import SimpleRentTest


class RentQueriesTestCase(SimpleRentTest):
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
                                "modelId": str(ob.publisher.id)
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
            variables={'id': str(self.property1.id)}
        )
        assert not executed.get("errors")
        expected = {
            "rentproperty": OrderedDict({
                "about": self.property1.about
            })
        }
        assert dict(executed.get("data")) == expected
