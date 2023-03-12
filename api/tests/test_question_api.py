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
    QuestionSerializer
)


QUESTIONS_URL = reverse('api:list-create-question')


def detail_url(pk):
    """Create and return a question detail URL."""
    return reverse('api:crud-question', args=[pk])


def create_company(user_id, **params):
    """Create and return a sample company."""
    defaults = {
        'name': 'Sample company name',
    }
    defaults.update(params)

    company = Company.objects.create(user_id=user_id, **defaults)
    return company


def create_question(user_id, **params):
    question = Question.objects.create(user_id=user_id, **params)
    return question


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
        sample_company = create_company(user_id=self.user, name='Samsung')
        payload = {
            'content': 'Sample question',
            'company_id': sample_company.id
        }
        res = self.client.post(QUESTIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        question = Question.objects.get(id=res.data['id'])
        self.assertEqual(question.user_id, self.user)

    
    def test_retrieve_questions(self):
        """Test retrieving a list of questions."""
        sample_company = create_company(user_id=self.user, name='Samsung')
        create_question(user_id=self.user, company_id=sample_company, content='Question One')
        create_question(user_id=self.user, company_id=sample_company, content='Question Two')

        res = self.client.get(QUESTIONS_URL)

        questions = Question.objects.all().order_by('-id')
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    
    def test_get_question_detail(self):
        """Test get question detail."""
        company = create_company(user_id=self.user)
        question = create_question(user_id=self.user, company_id=company, content='One Question')

        url = detail_url(question.id)
        res = self.client.get(url)

        serializer = QuestionSerializer(question)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    

    def test_partial_question_update(self):
        """Test partial update of a question."""
        company = create_company(
            user_id=self.user,
            name='Sample company title',
        )

        question = create_question(
            user_id=self.user,
            company_id=company,
            content='One Question'
        )
        payload = {'content': 'New question title'}
        url = detail_url(question.id)
        # res = self.client.put(url, payload)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        question.refresh_from_db()
        self.assertEqual(question.content, payload['content'])
        self.assertEqual(company.user_id, self.user)


    def test_delete_question(self):
        """Test deleting a question successful."""
        company = create_company(user_id=self.user)

        question = create_question(
            user_id=self.user,
            company_id=company,
            content='One Question'
        )

        url = detail_url(question.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(id=question.id).exists())





   