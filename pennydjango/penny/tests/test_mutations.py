from django.test import TestCase

from penny.models import User
from penny.tests.test_utils import GraphClientTestCase


class CreateUserTest(GraphClientTestCase):
    def test_create_user_mutation(self):

        data = {
            'username': 'testing',
            'password1': 'itsasecret',
            'password2': 'itsasecret',
            'email': 'test@test.com'
        }
        query = '''
            mutation createUserM($input: CreateUserInput!) {
              createUser(input: $input) {
                status
                formErrors
                user {
                  modelId
                }
              }
            }
            '''
        executed = self.client.execute(
            query,
            variables={'input': data},
            context=self.request
        )
        assert not executed.get('errors')
        res = executed['data']['createUser']
        assert res['status'] == 400,\
            "Should return 400 if there are form errors"
        assert 'email' in res['formErrors'], "Should have form error field"

        data['email'] = 'other@test.com'
        executed = self.client.execute(
            query,
            variables={'input': data},
            context=self.request
        )
        assert not executed.get('errors')
        res = executed['data']['createUser']
        assert res['status'] == 200,\
            "Should return 200 if mutation is successful"
        assert res['user']['modelId']
