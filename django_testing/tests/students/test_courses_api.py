import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from students.models import Course
from django_testing import settings


def test_example():
    assert True, "Just test example"


@pytest.mark.django_db
def test_courses_list(courses_factory, api_client):
    """проверка получения списка курсов (list-логика)"""
    course = courses_factory()
    url = reverse("courses-list")
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 1
    assert course.name == resp_json[0]['name']


@pytest.mark.django_db
def test_courses_retrieve(courses_factory, api_client):
    """проверка получения 1го курса (retrieve-логика)"""
    course = courses_factory()
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert course.name == resp_json['name']


@pytest.mark.django_db
def test_courses_create(api_client):
    """тест успешного создания курса"""
    course = Course.objects.create(name='Python-Developer')
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert course.name == 'Python-Developer'


@pytest.mark.django_db
def test_courses_update(courses_factory, api_client):
    """тест успешного обновления курса"""
    course = courses_factory()
    course.name = 'Что-то другое'
    course.save(update_fields=['name'])
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert course.name == 'Что-то другое'


@pytest.mark.django_db
def test_courses_delete(api_client):
    """тест успешного удаления курса"""
    course = Course.objects.create(name='Python-Developer')
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    Course.objects.get(name='Python-Developer').delete()
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp_json['detail'] == 'Not found.'


@pytest.mark.django_db
def test_courses_id_filter(api_client):
    """проверка фильтрации списка курсов по id"""
    Course.objects.create(name='Python-Developer')
    Course.objects.create(name='Java-Developer')
    Course.objects.create(name='C#-Developer')
    Course.objects.create(name='Android-Developer')
    url = "http://127.0.0.1:8000/api/v1/courses/?id=1&id=3"
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['name'] == 'Python-Developer' and resp_json[0]['id'] == 1
    assert resp_json[1]['name'] == 'C#-Developer' and resp_json[1]['id'] == 3


@pytest.mark.django_db
def test_courses_name_filter(api_client):
    """проверка фильтрации списка курсов по name"""
    Course.objects.create(name='Python-Developer')
    Course.objects.create(name='Java-Developer')
    Course.objects.create(name='C#-Developer')
    Course.objects.create(name='Android-Developer')
    url = "http://127.0.0.1:8000/api/v1/courses/?name=Java-Developer"
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['name'] == 'Java-Developer' and resp_json[0]['id'] == 2


"""тесты ограниченного числа студентов"""
@pytest.mark.parametrize("test_input, settings", [(25, settings.MAX_STUDENTS_PER_COURSE),
                                                  (0, settings.MAX_STUDENTS_PER_COURSE),
                                                  (15, settings.MAX_STUDENTS_PER_COURSE)])
def test_with_specific_settings(test_input, settings):
    assert test_input != settings


@pytest.mark.parametrize("test_input, settings", [(20, settings.MAX_STUDENTS_PER_COURSE)])
def test_with_specific_settings(test_input, settings):
    assert test_input == settings
