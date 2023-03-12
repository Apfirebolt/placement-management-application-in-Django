"""
Tests for offer APIs.
"""
from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Company, Offer
)

from api.serializers import (
    OfferSerializer
)


OFFERS_URL = reverse('api:list-create-offer')


def detail_url(pk):
    """Create and return a application detail URL."""
    return reverse('api:crud-offer', args=[pk])


def create_company(user_id, **params):
    """Create and return a sample company."""
    defaults = {
        'name': 'Sample company name',
    }
    defaults.update(params)

    company = Company.objects.create(user_id=user_id, **defaults)
    return company


def create_offer(user_id, **params):
    offer = Offer.objects.create(user_id=user_id, **params)
    return offer


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicOfferAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test no auth is required to call API."""
        res = self.client.get(OFFERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOfferApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
    

    def test_create_offer(self):
        """Test creating a Application."""
        sample_company = create_company(user_id=self.user, name='Samsung')
        payload = {
            'notes': 'Sample notes',
            'ctc': '18 LPA',
            'company_id': sample_company.id,
            'received_at': datetime.now()
        }
        res = self.client.post(OFFERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        offer = Offer.objects.get(id=res.data['id'])
        self.assertEqual(offer.user_id, self.user)
        self.assertEqual(offer.notes, payload['notes'])
        self.assertEqual(offer.ctc, payload['ctc'])
    
