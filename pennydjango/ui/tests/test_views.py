from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from penny.models import User
from rentals.tests.test_utils import SimpleRentTest


class SimpleViewTest(TestCase):
    """
    View method testing (http requests and view methods only)
    Use FrontendTest instead if you need websocket and http testing.

    Inherit from this test to create a test that checks View
    functionality against a mocked request

    Usage:
        class MyViewTest(ViewTest):
            VIEW_CLASS = MyView   # specify the view class you want to test

            def test_context(self):
                # self.view, self.request, self.user are automatically
                #   provided for convenience

                assert 'user' self.view.get_context(self.request)
    """
    VIEW_CLASS = None
    _VIEW = None
    _USER = None
    _REQUEST = None

    @property
    def url(self):
        return reverse(self.VIEW_CLASS.__name__)

    @property
    def view(self):
        self._VIEW = self._VIEW or self.VIEW_CLASS()
        return self._VIEW

    @property
    def user(self):
        self._USER = self._USER or User.objects.create_user(
            username='test_user',
            email='',
            password='correcthorsebatterystaple',
        )
        return self._USER

    def tearDown(self):
        User.objects.all().delete()


class DetailListingTest(SimpleRentTest, SimpleViewTest):

    def test_response(self):
        # Non logged in
        p_id = self.property1.id
        response = self.client.get(reverse('listing_detail',
                                           kwargs={'pk': p_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.login(username=self.test_user.username,
                          password='correcthorsebatterystaple')
        # Logged in
        response = self.client.get(reverse('listing_detail',
                                           kwargs={'pk': p_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['rentproperty'].id, p_id)
