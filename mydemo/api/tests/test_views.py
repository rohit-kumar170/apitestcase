from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import CustomUser
from api.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterViewTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('register')  # Assuming your URL name for RegisterView is 'register'
        data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'securepassword123',
        }

        # Make a POST request to the register endpoint
        response = self.client.post(url, data, format='json')

        # Assert that the request was successful (HTTP 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that a user was created with the provided data
        self.assertTrue(CustomUser.objects.filter(email='test@example.com').exists())

        # Assert that the response contains the user's details
        self.assertEqual(response.data['user']['email'], 'test@example.com')
        self.assertEqual(response.data['user']['first_name'], 'John')
        self.assertEqual(response.data['user']['last_name'], 'Doe')

        # You can add more assertions as needed based on your requirements




User = get_user_model()

class CustomLoginViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email='test@example.com', password='securepassword123')

    def test_login_success(self):
        url = '/api/login/'  # Ensure this matches your URL configuration
        data = {'email': 'test@example.com', 'password': 'securepassword123'}
        
        response = self.client.post(url, data, format='json')
        print("Response data", response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        
        # Optional: Check if the access token is in the expected JWT format
        import jwt
        try:
            jwt.decode(response.data['access'], options={"verify_signature": False})
            token_decoded = True
        except jwt.DecodeError:
            token_decoded = False
        self.assertTrue(token_decoded, "The access token is not a valid JWT")

    def test_login_failure(self):
        url = '/api/login/'  # Ensure this matches your URL configuration
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')
