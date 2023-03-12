"""
Tests for application APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Company, Application, Interview
)

from api.serializers import (
    InterviewSerializer
)


INTERVIEWS_URL = reverse('api:list-create-interview')


def detail_url(pk):
    """Create and return a interview detail URL."""
    return reverse('api:crud-interview', args=[pk])


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


def create_interview(application_id, **params):
    interview = Interview.objects.create(application_id=application_id, **params)
    return interview


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicInterviewAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test no auth is required to call API."""
        res = self.client.get(INTERVIEWS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInterviewApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
    

    


    