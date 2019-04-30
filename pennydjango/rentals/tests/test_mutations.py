# from rentals.tests.test_utils import SimpleRentTest
#
#
# class RentMutationsTestCase(SimpleRentTest):
#     def test_create_rentproperty_mutation(self):
#         data = {
#             "rentproperty": {
#                 "price": 2500,
#                 "contact": "me",
#                 "address": "my lil house",
#                 "latitude": 3.074567,
#                 "longitude": -76.5677,
#                 "about": "this is a nice house, don't u think? ;)",
#                 "bedrooms": 3,
#                 "baths": 2,
#                 "petsAllowed": True,
#                 "amenities": "a lot"
#             }
#         }
#         query = '''
#             mutation createRentP($input: CreateRentPropertyMutationInput!) {
#               createRentproperty(input: $input) {
#                 status
#                 formErrors
#                 rentproperty {
#                   id
#                 }
#               }
#             }
#             '''
#         executed = self.client.execute(
#             query,
#             variables={'input': data},
#             context=self.request
#         )
#         assert not executed.get('errors')
#         res = executed['data']['createRentproperty']
#         assert res['status'] == 403,\
#             "Testing user NOT authenticated but IT IS authenticated"
#
#         self.request.user = self.test_user
#         executed = self.client.execute(
#             query,
#             variables={'input': {}},
#             context=self.request
#         )
#         assert executed.get("errors"), "Should return errors"
#
#         executed = self.client.execute(
#             query,
#             variables={'input': data},
#             context=self.request
#         )
#         assert not executed.get("errors")
#         res = executed['data']['createRentproperty']
#         assert res['status'] == 200,\
#             "Should return 200 if mutation is successful"
#         assert res['rentproperty']['id']
#
#         data["rentproperty"]['latitude'] = 33.1111111111
#         executed = self.client.execute(
#             query,
#             variables={'input': data},
#             context=self.request
#         )
#
#         assert not executed.get("errors")
#         res = executed['data']['createRentproperty']
#         assert res['status'] == 400,\
#             "Should return 400 if there are form errors"
#         assert 'latitud' in res['formErrors'], "Should have form error field"
