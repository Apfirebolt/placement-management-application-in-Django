"""
Tests for application APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Company, Application
)

from api.serializers import (
    ApplicationSerializer
)


APPLICATIONS_URL = reverse('api:list-create-application')


def detail_url(pk):
    """Create and return a application detail URL."""
    return reverse('api:crud-application', args=[pk])


def create_company(user_id, **params):
    """Create and return a sample company."""
    defaults = {
        'name': 'Sample company name',
    }
    defaults.update(params)

    company = Company.objects.create(user_id=user_id, **defaults)
    return company


def create_application(user_id, **params):
    application = Application.objects.create(user_id=user_id, **params)
    return application


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicQuestionAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test no auth is required to call API."""
        res = self.client.get(APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatequestionApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
    

    def test_create_application(self):
        """Test creating a Application."""
        sample_company = create_company(user_id=self.user, name='Samsung')
        payload = {
            'notes': 'Sample notes',
            'source': 'Sample source',
            'company_id': sample_company.id
        }
        res = self.client.post(APPLICATIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        application = Application.objects.get(id=res.data['id'])
        self.assertEqual(application.user_id, self.user)
        self.assertEqual(application.notes, payload['notes'])
    





   