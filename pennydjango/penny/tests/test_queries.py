from collections import OrderedDict

from penny import queries
from penny.tests.test_utils import GraphClientTestCase


class RentQueriesTestCase(GraphClientTestCase):
    def test_rentproperty_type(self):
        instance = queries.UserType()
        self.assertIsNotNone(instance)

    def test_resolve_all_users(self):
        executed = self.client.execute(
            '''
            query {
              allUsers{
                edges{
                  node{
                    username
                  }
                }
              }
            }
            '''
        )
        self.assertIsNone(executed.get("errors"))
        expected = {
            "allUsers": OrderedDict({
                "edges": [
                    OrderedDict({
                        "node": OrderedDict({
                            "username": self.test_user.username,
                        })
                    })
                ]
            })
        }
        self.assertEqual(dict(executed.get("data")), expected)

    def test_resolve_user(self):
        executed = self.client.execute(
            '''
            query getUser($id: UUID!){
              user(modelId: $id){
                username
              }
            }
            ''',
            variables={'id': str(self.test_user.model_id)}
        )
        self.assertIsNone(executed.get("errors"))
        expected = {
            "user": OrderedDict({
                "username": self.test_user.username
            })
        }
        self.assertEqual(dict(executed.get("data")), expected)
