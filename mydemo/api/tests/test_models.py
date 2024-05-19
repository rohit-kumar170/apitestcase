from django.test import TestCase
from api.models import CustomUser
from django.db.utils import IntegrityError

class CustomUserManagerTestCase(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='securepassword123'
        )
        self.assertTrue(user.pk)
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertIsNotNone(user.date_joined)
        
    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='supersecurepassword123'
        )
        self.assertTrue(superuser.pk)
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertIsNotNone(superuser.date_joined)
        
    def test_missing_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='test123')
            
    def test_email_uniqueness(self):
        # Create a user with a specific email
        CustomUser.objects.create_user(email='test@example.com', password='test123')
        
        # Try to create another user with the same email, should raise IntegrityError
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(email='test@example.com', password='test456')
