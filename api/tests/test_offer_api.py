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

    
    def test_retrieve_offers(self):
        """Test retrieving a list of offers."""
        sample_company = create_company(user_id=self.user, name='Samsung')
        create_offer(user_id=self.user, company_id=sample_company, notes='Note One', ctc='10 LPA', received_at=datetime.now())
        create_offer(user_id=self.user, company_id=sample_company, notes='Note Two', ctc='22 LPA', received_at=datetime.now())

        res = self.client.get(OFFERS_URL)

        applications = Offer.objects.all().order_by('-id')
        serializer = OfferSerializer(applications, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)
    

    def test_get_offer_detail(self):
        """Test get offer detail."""
        company = create_company(user_id=self.user)
        offer = create_offer(user_id=self.user, company_id=company, notes='Note Two', ctc='22 LPA', received_at=datetime.now())

        url = detail_url(offer.id)
        res = self.client.get(url)

        serializer = OfferSerializer(offer)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    
    def test_partial_offer_update(self):
        """Test partial update of an offer."""
        company = create_company(
            user_id=self.user,
            name='Sample company title',
        )

        offer = create_offer(user_id=self.user, company_id=company, notes='Note Two', ctc='22 LPA', received_at=datetime.now())

        payload = {'ctc': '40 LPA'}
        url = detail_url(offer.id)
        # res = self.client.put(url, payload)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        offer.refresh_from_db()
        self.assertEqual(offer.ctc, payload['ctc'])
        self.assertEqual(offer.user_id, self.user)


    def test_delete_offer(self):
        """Test deleting an offer successful."""
        company = create_company(user_id=self.user)

        offer = create_offer(user_id=self.user, company_id=company, notes='Note Two', ctc='22 LPA', received_at=datetime.now())

        url = detail_url(offer.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=offer.id).exists())