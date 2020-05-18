from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.
CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(params)


class PublicUserApiTests(TestCase):
    """Teste the users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload"""

        payload = {
            'email': 'john.doe@email.com',
            'password': 'q1w2e3r4',
            'name': 'John Doe',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        
    
    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """Test that password must be more than 8 characters"""
        payload = {
            'email': 'john.doe@email.com',
            'password': 'q1w2',
            'name': 'John Doe',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)
        