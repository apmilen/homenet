from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from penny.models import User
from penny.forms import UserProfileForm


class UserProfileTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            email='test@test.com',
            username='test_pub',
            password='alalalalong'
        )
        self.pic_path = 'pennydjango/static/images/blank-profile-picture.png'

    def test_profile(self):
        response = self.client.get(reverse(
            'userprofile', args=[self.test_user.username]))
        self.assertContains(response, self.test_user.avatar_url)
        self.assertContains(response, self.test_user.first_name)
        self.assertContains(response, self.test_user.email)

    def test_profile_form(self):
        with open(self.pic_path, 'rb') as pic_file:
            uploaded_file = SimpleUploadedFile(pic_file.name, pic_file.read())
            form = UserProfileForm(
                {'first_name': 'Sammuels'},
                {'file': uploaded_file}
            )
            self.assertTrue(form.is_valid())

    def test_post(self):
        self.client.login(username='test_pub', password='alalalalong')
        post_endpoint = reverse('userprofile', args=[self.test_user.username])
        with open(self.pic_path, 'rb') as pic_file:
            post_data = {
                'type': 'edit_profile',
                'avatar': pic_file,
                'first_name': 'Portugal'
            }
            response = self.client.post(post_endpoint, post_data)
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.first_name, 'Portugal')
        self.assertEqual(
            self.test_user.avatar_url,
            f"/media/{str(self.test_user.id)}/avatar.png"
        )

    def tearDown(self):
        self.test_user.delete()
