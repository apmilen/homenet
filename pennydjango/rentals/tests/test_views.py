from http import HTTPStatus
from django.urls import reverse

from rentals.tests.test_utils import SimpleRentTest
from rentals.forms import RentPropertyForm


class DetailListingTest(SimpleRentTest):
    def test_response(self):
        # Non logged in
        p_id = self.property1.id
        response = self.client.get(reverse('listing_detail',
                                           kwargs={'pk': p_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Logged in
        self.client.login(username=self.test_user.username,
                          password='correcthorsebatterystaple')
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
        form = RentPropertyForm({
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
