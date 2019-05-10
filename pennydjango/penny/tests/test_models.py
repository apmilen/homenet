from django.test import TestCase

from penny.constants import USER_TYPE, AGENT_TYPE, ADMIN_TYPE, CLIENT_TYPE
from penny.models import User, PermissionManager


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


class UserManagerTestCase(TestCase):
    def test_create_usertype(self):
        # Agent
        agent = User.objects.create_agent(
            username='agent',
            password='123',
            email='agent@ag.co'
        )
        self.assertEqual(agent.user_type, AGENT_TYPE)

        # Client
        client = User.objects.create_client(
            username='client',
            password='123',
            email='client@cl.co'
        )
        self.assertEqual(client.user_type, CLIENT_TYPE)

        # Admin
        admin = User.objects.create_admin(
            username='admin',
            password='123',
            email='agent@adm.co'
        )
        self.assertEqual(admin.user_type, ADMIN_TYPE)


class PermissionManagerTestCase(TestCase):
    def setUp(self):
        super().setUp()
        # Agent
        self.user_agent = User.objects.create_agent(
            username='agent',
            password='123',
            email='agent@ag.co'
        )
        # Client
        self.user_client = User.objects.create_client(
            username='client',
            password='123',
            email='client@cl.co'
        )
        # Admin
        self.user_admin = User.objects.create_admin(
            username='admin',
            password='123',
            email='agent@adm.co'
        )

    def tearDown(self):
        self.user_agent.delete()
        self.user_client.delete()
        self.user_admin.delete()

    def test_perms(self):
        # Agent perms
        self.assertEqual(type(self.user_agent.perms), PermissionManager)
        self.assertTrue(self.user_agent.perms.has_agent_access())
        self.assertTrue(self.user_agent.perms.has_client_or_agent_access())
        self.assertFalse(self.user_agent.perms.has_admin_access())
        self.assertFalse(self.user_agent.perms.has_client_access())

        # Client perms
        self.assertEqual(type(self.user_client.perms), PermissionManager)
        self.assertTrue(self.user_client.perms.has_client_access())
        self.assertTrue(self.user_client.perms.has_client_or_agent_access())
        self.assertFalse(self.user_client.perms.has_agent_access())
        self.assertFalse(self.user_client.perms.has_admin_access())

        # Admin perms
        self.assertEqual(type(self.user_admin.perms), PermissionManager)
        self.assertTrue(self.user_admin.perms.has_client_access())
        self.assertTrue(self.user_admin.perms.has_client_or_agent_access())
        self.assertTrue(self.user_admin.perms.has_agent_access())
        self.assertTrue(self.user_admin.perms.has_admin_access())
