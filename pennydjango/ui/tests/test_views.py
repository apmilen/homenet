from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from penny.models import User
from rentals.tests.test_utils import SimpleRentTest
from rentals.forms import CreateRentPropertyForm


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


class RentPropertyTest(SimpleRentTest):
    def test_view(self):
        creation_link = reverse('admin:rentals_rentproperty_add')
        response = self.client.post(creation_link)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.client.login(
            username=self.test_user.username, password='alalalalong'))
        response = self.client.post(creation_link)
        self.assertEqual(response.status_code, 302)

        self.test_user.is_staff = True
        self.test_user.is_superuser = True
        self.test_user.save()

        self.client.logout()
        self.client.login(
            username=self.test_user.username, password='alalalalong')
        response = self.client.get(creation_link)
        self.assertEqual(response.status_code, 200)

    def test_form(self):
        form = CreateRentPropertyForm({
            'is_listed': True,
            'price': 999,
            'contact': 'bob at 018000-marley',
            'address': '420 love street',
            'geopoint': "POINT (-73.92617910000001 40.7106363)",
            'about': 'no roof so you can view the stars at night',
            'amenities': 'windows,doors,garden',
            'bedrooms': 3,
            'baths': 2,
        })
        self.assertTrue(form.is_valid())
