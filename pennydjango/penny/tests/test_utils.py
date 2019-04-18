from graphene.test import Client
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test import RequestFactory

from penny.models import User
from penny.schema import schema


class GraphClientTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            email='test@test.com',
            username='test_pub',
            password='alalalalong'
        )
        self.client = Client(schema)
        self.request = RequestFactory().get('/')
        self.request.user = AnonymousUser()

    def tearDown(self):
        self.test_user.delete()
