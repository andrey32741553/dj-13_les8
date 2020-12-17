import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from django_testing import settings


@pytest.fixture
def courses_factory():
    def factory(**kwargs):
        course = baker.make('students.Course', **kwargs)
        return course
    return factory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def settings():
    return settings
