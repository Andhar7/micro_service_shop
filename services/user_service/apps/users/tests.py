from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import UserProfile
from apps.users.serializers import UserRegistrationSerializer, UserWithProfileSerializer
import json

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """Test creating a user with valid data"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = User.objects.create_superuser(**self.user_data)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_as_username_field(self):
        """Test that email is used as USERNAME_FIELD"""
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_required_fields(self):
        """Test required fields"""
        expected_fields = ['username', 'first_name', 'last_name']
        self.assertEqual(User.REQUIRED_FIELDS, expected_fields)


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

    def test_create_user_profile(self):
        """Test creating a user profile"""
        profile_data = {
            'phone': '+1234567890',
            'address': '123 Test St, Test City',
            'date_of_birth': '1990-01-01'
        }
        profile = UserProfile.objects.create(user=self.user, **profile_data)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, profile_data['phone'])
        self.assertEqual(profile.address, profile_data['address'])
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)

    def test_user_profile_str_representation(self):
        """Test string representation of UserProfile"""
        profile = UserProfile.objects.create(user=self.user)
        expected_str = f"Profile of {self.user.email}"
        self.assertEqual(str(profile), expected_str)

    def test_profile_cascade_delete(self):
        """Test that profile is deleted when user is deleted"""
        profile = UserProfile.objects.create(user=self.user)
        user_id = self.user.id
        profile_id = profile.id

        self.user.delete()

        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(UserProfile.objects.filter(id=profile_id).exists())


class UserRegistrationAPITest(APITestCase):
    """Test cases for user registration API"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.valid_user_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }

    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['email'], self.valid_user_data['email'])
        self.assertEqual(response.data['username'], self.valid_user_data['username'])
        self.assertEqual(response.data['message'], 'User registered successfully')

        # Verify user was created in database
        user = User.objects.get(email=self.valid_user_data['email'])
        self.assertEqual(user.username, self.valid_user_data['username'])

        # Verify profile was created
        self.assertTrue(hasattr(user, 'profile'))

    def test_register_user_password_mismatch(self):
        """Test registration with password mismatch"""
        invalid_data = self.valid_user_data.copy()
        invalid_data['password_confirm'] = 'differentpass'

        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_confirm', response.data)

    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email"""
        # Create a user first
        User.objects.create_user(
            email=self.valid_user_data['email'],
            username='firstuser',
            password='pass123'
        )

        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_user_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create a user first
        User.objects.create_user(
            email='different@example.com',
            username=self.valid_user_data['username'],
            password='pass123'
        )

        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_user_weak_password(self):
        """Test registration with weak password"""
        invalid_data = self.valid_user_data.copy()
        invalid_data['password'] = '123'
        invalid_data['password_confirm'] = '123'

        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_user_missing_required_fields(self):
        """Test registration with missing required fields"""
        incomplete_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }

        response = self.client.post(self.register_url, incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileAPITest(APITestCase):
    """Test cases for user profile API"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='+1234567890',
            address='123 Test St'
        )

        # Create JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.profile_url = reverse('profile')
        self.profile_update_url = reverse('profile-update')

    def test_get_user_profile_authenticated(self):
        """Test retrieving user profile when authenticated"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertIn('profile', response.data)
        self.assertEqual(response.data['profile']['phone'], '+1234567890')

    def test_get_user_profile_unauthenticated(self):
        """Test retrieving user profile when not authenticated"""
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile_success(self):
        """Test successful profile update"""
        update_data = {
            'phone': '+9876543210',
            'address': '456 New Address St',
            'date_of_birth': '1990-01-01'
        }

        response = self.client.put(self.profile_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, update_data['phone'])
        self.assertEqual(self.profile.address, update_data['address'])

    def test_update_user_profile_partial(self):
        """Test partial profile update"""
        update_data = {'phone': '+5555555555'}

        response = self.client.patch(self.profile_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify only phone was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, update_data['phone'])
        self.assertEqual(self.profile.address, '123 Test St')  # Should remain unchanged

    def test_update_user_profile_unauthenticated(self):
        """Test profile update when not authenticated"""
        self.client.credentials()  # Remove authentication
        update_data = {'phone': '+9999999999'}

        response = self.client.put(self.profile_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_profile_if_not_exists(self):
        """Test that profile is created if it doesn't exist during update"""
        # Create a user without profile
        user_without_profile = User.objects.create_user(
            email='noprofile@example.com',
            username='noprofile',
            password='testpass123'
        )

        # Create new token for this user
        refresh = RefreshToken.for_user(user_without_profile)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        update_data = {'phone': '+1111111111', 'address': 'New Address'}
        response = self.client.put(self.profile_update_url, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify profile was created
        self.assertTrue(UserProfile.objects.filter(user=user_without_profile).exists())


class UserSerializerTest(TestCase):
    """Test cases for user serializers"""

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }

    def test_user_registration_serializer_valid(self):
        """Test UserRegistrationSerializer with valid data"""
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_user_registration_serializer_password_mismatch(self):
        """Test UserRegistrationSerializer with password mismatch"""
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'differentpass'

        serializer = UserRegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_confirm', serializer.errors)

    def test_user_registration_serializer_create(self):
        """Test UserRegistrationSerializer create method"""
        serializer = UserRegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        # Verify profile was created
        self.assertTrue(hasattr(user, 'profile'))

    def test_user_with_profile_serializer(self):
        """Test UserWithProfileSerializer"""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        UserProfile.objects.create(
            user=user,
            phone='+1234567890',
            address='Test Address'
        )

        serializer = UserWithProfileSerializer(user)
        self.assertIn('profile', serializer.data)
        self.assertEqual(serializer.data['profile']['phone'], '+1234567890')


class AuthenticationIntegrationTest(APITestCase):
    """Integration tests for authentication flow"""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'integration@example.com',
            'username': 'integrationuser',
            'first_name': 'Integration',
            'last_name': 'Test',
            'password': 'integrationpass123',
            'password_confirm': 'integrationpass123'
        }
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')
        self.profile_update_url = reverse('profile-update')

    def test_full_user_workflow(self):
        """Test complete user workflow: register -> authenticate -> profile operations"""
        # 1. Register user
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['id']

        # 2. Get user for token generation (simulating login)
        user = User.objects.get(id=user_id)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # 3. Authenticate and get profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

        # 4. Update profile
        update_data = {
            'phone': '+1111111111',
            'address': 'Integration Test Address',
            'date_of_birth': '1985-05-15'
        }
        response = self.client.put(self.profile_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 5. Verify profile was updated
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['phone'], update_data['phone'])
        self.assertEqual(response.data['profile']['address'], update_data['address'])