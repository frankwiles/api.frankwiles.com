from test_plus import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..factories import UserFactory, StaffUserFactory, SuperUserFactory

User = get_user_model()


class UserModelTests(TestCase):
    def test_simple_user_creation(self):
        """Test simple user creation"""
        now = timezone.now()
        f = UserFactory()
        self.assertTrue(f.is_active)

        # Ensure LastSeen model is created
        self.assertTrue(f.last_seen.at > now)

    def test_staff_creation(self):
        """Test simple staff creation"""
        s = StaffUserFactory()
        self.assertTrue(s.is_active)
        self.assertTrue(s.is_staff)
        self.assertFalse(s.is_superuser)

    def test_superuser_creation(self):
        """Test simple superuser creation"""
        s = SuperUserFactory()
        self.assertTrue(s.is_active)
        self.assertTrue(s.is_staff)
        self.assertTrue(s.is_superuser)


class UserManagerTests(TestCase):
    def test_record_login_email(self):
        """Test logging in via email"""
        user = UserFactory()
        now = timezone.now()
        self.assertTrue(user.last_login < now)
        User.objects.record_login(email=user.email)

        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.last_login > now)

    def test_record_login_user(self):
        """Test recordingn last login"""
        user = UserFactory()
        now = timezone.now()
        self.assertTrue(user.last_login < now)
        User.objects.record_login(user=user)

        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.last_login > now)

    def test_create_user(self):
        """Test create_user"""
        u = User.objects.create_user("t1@example.com", "t1pass")
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_staff)
        self.assertFalse(u.is_superuser)

    def test_create_staffuser(self):
        """Test create_staffuser"""
        u = User.objects.create_staffuser("t1@example.com", "t1pass")
        self.assertTrue(u.is_active)
        self.assertTrue(u.is_staff)
        u = User.objects.create_staffuser("t2@example.com", "t2pass")
        self.assertTrue(u.is_active)
        self.assertTrue(u.is_staff)
        self.assertFalse(u.is_superuser)

    def test_create_superuser(self):
        """Test create_superuser"""
        u = User.objects.create_superuser("t3@example.com", "t3pass")
        self.assertTrue(u.is_active)
        self.assertTrue(u.is_staff)
        self.assertTrue(u.is_superuser)
