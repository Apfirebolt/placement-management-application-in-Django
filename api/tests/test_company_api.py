"""
Tests for company APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Company,
)

from api.serializers import (
    CompanySerializer,
)


COMPANIES_URL = reverse('api:list-create-company')


def detail_url(pk):
    """Create and return a company detail URL."""
    return reverse('api:crud-company', args=[pk])


def create_company(user_id, **params):
    """Create and return a sample company."""
    defaults = {
        'name': 'Sample company name',
    }
    defaults.update(params)

    company = Company.objects.create(user_id=user_id, **defaults)
    return company


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicCompanyAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test no auth is required to call API."""
        res = self.client.get(COMPANIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCompanyApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_companies(self):
        """Test retrieving a list of companies."""
        create_company(user_id=self.user, name='Samsung')
        create_company(user_id=self.user, name='Nokia')

        res = self.client.get(COMPANIES_URL)

        companies = Company.objects.all().order_by('-id')
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)
    

    def test_create_company(self):
        """Test creating a company."""
        payload = {
            'name': 'Sample company',
        }
        res = self.client.post(COMPANIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Company.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user_id, self.user)

    
    def test_get_company_detail(self):
        """Test get company detail."""
        company = create_company(user_id=self.user)

        url = detail_url(company.id)
        res = self.client.get(url)

        serializer = CompanySerializer(company)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_partial_company_update(self):
        """Test partial update of a company."""
        company = create_company(
            user_id=self.user,
            name='Sample company title',
        )

        payload = {'name': 'New company title'}
        url = detail_url(company.id)
        res = self.client.put(url, payload)
        # res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertEqual(company.name, payload['name'])
        self.assertEqual(company.user_id, self.user)

    
    def test_delete_company(self):
        """Test deleting a company successful."""
        company = create_company(user_id=self.user)

        url = detail_url(company.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company.id).exists())


   