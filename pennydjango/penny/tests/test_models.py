from django.test import TestCase

from penny.constants import USER_TYPE
from penny.models import User


class UserTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='test',
            password='test',
            user_type='agent',
            email='test@test.com'
        )

    def tearDown(self):
        super().tearDown()
        del self.user

    def test_usertype(self):
        """
        Tests that a user can only be one user type
        """

        for usertype_pair in USER_TYPE:
            usertype = usertype_pair[0]
            self.user.user_type = usertype
            self.user.save()
            # Assert it is its BD type
            self.assertTrue(getattr(self.user, f'is_user_{usertype}'))
            for usertype_pair2 in USER_TYPE:
                usertype2 = usertype_pair2[0]
                if usertype != usertype2:
                    # Assert is not other user type
                    self.assertFalse(getattr(self.user, f'is_user_{usertype2}'))
