"""
Tests for application APIs.
"""
import os
import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Company, Resume
)

from api.serializers import (
    ResumeSerializer
)


RESUME_URL = reverse('api:list-create-resume')


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


class PublicResumeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test no auth is required to call API."""
        res = self.client.get(RESUME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateResumeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)


    def test_create_resume(self):
        """Test creating a Resume."""
        sample_company = create_company(user_id=self.user, name='Samsung')

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'resume': image_file, 'company_id': sample_company.id}
            res = self.client.post(RESUME_URL, payload, format='multipart')
      

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        resume = Resume.objects.get(id=res.data['id'])
        self.assertEqual(resume.user_id, self.user)
        self.assertTrue(os.path.exists(resume.resume.path))
    

   