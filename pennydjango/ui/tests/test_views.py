from django.urls import reverse
from django.test import TestCase

from penny.constants import CLIENT_TYPE
from penny.models import User


class UserSignupTest(TestCase):
    def test_signup(self):
        data = {
            'username': 'juan',
            'password1': 'Jad33rf3r4f4',
            'password2': 'Jad33rf3r4f4'
        }
        response = self.client.post(reverse('signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='juan').exists())

        data['email'] = 'juan@jn.co'
        response = self.client.post(reverse('signup'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='juan').exists())
        u = User.objects.get(username='juan')
        self.assertEqual(u.user_type, CLIENT_TYPE)
