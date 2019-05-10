import random

from django.urls import reverse
from django.test import TestCase

from penny.constants import NEIGHBORHOODS, DAYS, AGENT_TYPE, CLIENT_TYPE
from penny.models import User
from schedule.models import Availability
from schedule.forms import AvailabilityForm


class ScheduleTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            email='test@test.com',
            username='test_pub',
            password='test',
            user_type=AGENT_TYPE
        )
        self.test_user_2 = User.objects.create_user(
            email='test2@test.com',
            username='test_pub2',
            password='test',
            user_type=AGENT_TYPE
        )
        self.test_user_3 = User.objects.create_user(
            email='test3@test.com',
            username='test_pub3',
            password='test',
            user_type=CLIENT_TYPE
        )
        self.form_data = {
            'neighborhood': random.choice(random.choice(NEIGHBORHOODS)[1])[0],
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

    def test_view_post(self):
        # non logged in
        response = self.client.post(reverse('schedule'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/schedule/")

        # Client logged in
        self.client.login(username='test_pub3', password='test')
        response = self.client.post(reverse('schedule'))
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # Agent logged in
        self.client.login(username='test_pub', password='test')
        response = self.client.post(reverse('schedule'), self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/schedule/")

        obj = Availability.objects.get()
        self.assertEqual(obj.agent.username, self.test_user.username)
        self.assertEqual(obj.neighborhood, self.form_data['neighborhood'])
        self.assertEqual(obj.start_day, self.form_data['start_day'])
        self.assertEqual(obj.end_day, self.form_data['end_day'])
        self.assertEqual(
            obj.start_time.strftime('%H:%M'), self.form_data['start_time']
        )
        self.assertEqual(
            obj.end_time.strftime('%H:%M'), self.form_data['end_time']
        )
        self.assertEqual(obj.agent_id, self.test_user.id)

    def test_delete(self):
        obj = Availability.objects.create(
            agent=self.test_user, **self.form_data)

        response = self.client.post(reverse('schedule-delete', args=[obj.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Availability.objects.filter(id=obj.id).exists())

        # non logged in
        self.client.login(
            username=self.test_user_2.username, password='test')
        response = self.client.post(reverse('schedule-delete', args=[obj.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Availability.objects.filter(id=obj.id).exists())

        # Client logged in
        self.client.login(username='test_pub3', password='test')
        response = self.client.post(reverse('schedule-delete', args=[obj.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Availability.objects.filter(id=obj.id).exists())
        self.client.logout()

        # Agent logged in
        self.client.login(
            username=self.test_user.username, password='test')
        response = self.client.post(reverse('schedule-delete', args=[obj.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Availability.objects.filter(id=obj.id).exists())

    def tearDown(self):
        User.objects.all().delete()
        Availability.objects.all().delete()
