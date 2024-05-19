from django.test import TestCase
from api.serializers import RegisterSerializer
from api.models import CustomUser

class RegisterSerializerTestCase(TestCase):
    def test_valid_data(self):
        serializer = RegisterSerializer(data={
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'securepassword123'
        })
        self.assertTrue(serializer.is_valid())
        
    def test_missing_fields(self):
        serializer = RegisterSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('password', serializer.errors)

    def test_invalid_email(self):
        serializer = RegisterSerializer(data={
            'email': 'invalid_email',
            'password': 'securepassword123'
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_create_user(self):
        serializer = RegisterSerializer(data={
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'securepassword123'
        })
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Check if the user is saved to the database
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('securepassword123'))

        # Make sure the user is an instance of CustomUser model
        self.assertIsInstance(user, CustomUser)
