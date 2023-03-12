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


class PublicApplicationAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test no auth is required to call API."""
        res = self.client.get(APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApplicationApiTests(TestCase):
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
    

    def test_retrieve_applications(self):
        """Test retrieving a list of applications."""
        sample_company = create_company(user_id=self.user, name='Samsung')
        create_application(user_id=self.user, company_id=sample_company, notes='Note One', source='Source One')
        create_application(user_id=self.user, company_id=sample_company, notes='Note Two', source='Source Two')

        res = self.client.get(APPLICATIONS_URL)

        applications = Application.objects.all().order_by('-id')
        serializer = ApplicationSerializer(applications, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)


    def test_get_application_detail(self):
        """Test get application detail."""
        company = create_company(user_id=self.user)
        application = create_application(user_id=self.user, company_id=company, notes='One Note', source='One Source')

        url = detail_url(application.id)
        res = self.client.get(url)

        serializer = ApplicationSerializer(application)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    

    def test_partial_application_update(self):
        """Test partial update of an application."""
        company = create_company(
            user_id=self.user,
            name='Sample company title',
        )

        application = create_application(
            user_id=self.user,
            company_id=company,
            notes='One Note',
            source='One Source'
        )
        payload = {'source': 'New source'}
        url = detail_url(application.id)
        # res = self.client.put(url, payload)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        application.refresh_from_db()
        self.assertEqual(application.source, payload['source'])
        self.assertEqual(company.user_id, self.user)


    def test_delete_application(self):
        """Test deleting an application successful."""
        company = create_company(user_id=self.user)

        application = create_application(
            user_id=self.user,
            company_id=company,
            notes='One Note',
            source='One Source'
        )

        url = detail_url(application.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Application.objects.filter(id=application.id).exists())
   