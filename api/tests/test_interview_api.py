"""
Tests for interview APIs.
"""
from datetime import datetime
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


    def test_create_interview(self):
        """Test creating an interview."""
        sample_company = create_company(user_id=self.user, name='Samsung')
        sample_application = create_application(
            user_id=self.user,
            notes='Sample Notes',
            source='Sample Source',
            company_id=sample_company
        )

        payload = {
            'application_id': sample_application.id,
            'notes': 'Some interview notes',
            'round': 'Second Round',
            'result': 'Passed',
            'scheduled_at': datetime.now()
        }

        res = self.client.post(INTERVIEWS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        interview = Interview.objects.get(id=res.data['id'])
        self.assertEqual(interview.application_id, sample_application)
        self.assertEqual(interview.notes, payload['notes'])

    
    def test_retrieve_interviews(self):
        """Test retrieving a list of interviews."""
        sample_company = create_company(user_id=self.user, name='Samsung')
        sample_application = create_application(
            user_id=self.user,
            notes='Sample Notes',
            source='Sample Source',
            company_id=sample_company
        )
        create_interview(application_id=sample_application, round='First Round', notes='Note Two', result='Passed', scheduled_at=datetime.now())
        create_interview(application_id=sample_application, round='Second Round', notes='Note One', result='Failed', scheduled_at=datetime.now())

        res = self.client.get(INTERVIEWS_URL)

        interviews = Interview.objects.all().order_by('-id')
        serializer = InterviewSerializer(interviews, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    
    def test_get_interview_detail(self):
        """Test get interview detail."""
        company = create_company(user_id=self.user)
        application = create_application(user_id=self.user, company_id=company, notes='One Note', source='One Source')
        interview = create_interview(application_id=application, round='First Round', notes='Note Two', result='Passed', scheduled_at=datetime.now())

        url = detail_url(interview.id)
        res = self.client.get(url)

        serializer = InterviewSerializer(interview)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    
    def test_partial_application_update(self):
        """Test partial update of an interview."""
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

        interview = create_interview(
            application_id=application, 
            round='First Round', 
            notes='Note Two', 
            result='Passed', 
            scheduled_at=datetime.now()
        )
        payload = {'result': 'Failed'}
        url = detail_url(interview.id)
        # res = self.client.put(url, payload)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        interview.refresh_from_db()
        self.assertEqual(interview.result, payload['result'])
        self.assertEqual(interview.application_id, application)

    
    def test_delete_interview(self):
        """Test deleting an intervoew successful."""
        company = create_company(user_id=self.user)

        application = create_application(
            user_id=self.user,
            company_id=company,
            notes='One Note',
            source='One Source'
        )

        interview = create_interview(
            application_id=application, 
            round='First Round', 
            notes='Note Two', 
            result='Passed', 
            scheduled_at=datetime.now()
        )

        url = detail_url(interview.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Interview.objects.filter(id=interview.id).exists())


    