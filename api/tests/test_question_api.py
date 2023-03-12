"""
Tests for question APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Company, Question
)

from api.serializers import (
    CompanySerializer, QuestionSerializer
)


COMPANIES_URL = reverse('api:list-create-company')
QUESTIONS_URL = reverse('api:list-create-question')


def detail_url(pk):
    """Create and return a question detail URL."""
    return reverse('api:crud-question', args=[pk])


def create_company(user_id, **params):
    """Create and return a sample question."""
    defaults = {
        'name': 'Sample company name',
    }
    defaults.update(params)

    company = Company.objects.create(user_id=user_id, **defaults)
    return company


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicQuestionAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test no auth is required to call API."""
        res = self.client.get(QUESTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatequestionApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
    

    def test_create_question(self):
        """Test creating a Question."""
        sampleCompany = create_company(user_id=self.user, name='Samsung')
        payload = {
            'content': 'Sample question',
            'company_id': sampleCompany.id
        }
        res = self.client.post(QUESTIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        question = Question.objects.get(id=res.data['id'])
        self.assertEqual(question.user_id, self.user)

    
    



   