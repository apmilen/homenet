import random

from django.urls import reverse
from django.test import TestCase

from penny.models import User, Availability
from penny.constants import NEIGHBORHOODS, DAYS
from penny.forms import AvailabilityForm


class ScheduleTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            email='test@test.com',
            username='test_pub',
            password='alalalalong'
        )
        self.form_data = {
            'neighborhood': random.choice(NEIGHBORHOODS)[0],
            'start_day': random.choice(DAYS),
            'end_day': random.choice(DAYS),
            'start_time': '08:20',
            'end_time': '14:00',
        }

    def test_form(self):
        form = AvailabilityForm(self.form_data)
        self.assertTrue(form.is_valid())

        form2 = AvailabilityForm({
            'neighborhood': 'patagonia',
            'start_day': 'mars',
            'end_day': 'moon',
            'start_time': '18:20',
            'end_time': '14:00',
        })
        self.assertFalse(form2.is_valid())

        error_keys = {'neighborhood', 'start_day', 'end_day', 'end_time'}
        assert error_keys.issubset(form2.errors)

    def test_view(self):
        response = self.client.post(reverse('schedule'))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='test_pub', password='alalalalong')
        response = self.client.post(reverse('schedule'), self.form_data)
        self.assertEqual(response.status_code, 302)

        obj = Availability.objects.get()
        self.assertEqual(obj.agent.username, self.test_user.username)
        self.assertEqual(obj.neighborhood, self.form_data['neighborhood'])
        self.assertEqual(obj.start_day, self.form_data['start_day'])
        self.assertEqual(obj.end_day, self.form_data['end_day'])
        self.assertEqual(
            obj.start_time.strftime('%H:%M'), self.form_data['start_time'])
        self.assertEqual(
            obj.end_time.strftime('%H:%M'), self.form_data['end_time'])

    def tearDown(self):
        self.test_user.delete()
        Availability.objects.all().delete()
