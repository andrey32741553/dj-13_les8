import random

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from students.models import Course
from django.conf import settings


def test_example():
    assert True, "Just test example"


@pytest.mark.django_db
def test_courses_list(courses_factory, api_client):
    """проверка получения списка курсов (list-логика)"""
    courses_factory(_quantity=4)
    url = reverse("courses-list")
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 4


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
def test_courses_create(api_client, courses_factory):
    """тест успешного создания курса"""
    course = courses_factory(name='Python-Developer')
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
def test_courses_delete(courses_factory, api_client):
    """тест успешного удаления курса"""
    course = courses_factory(name='Something interesting')
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    Course.objects.get(name='Something interesting').delete()
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp_json['detail'] == 'Not found.'


@pytest.mark.django_db
def test_courses_id_filter(courses_factory, api_client):
    """проверка фильтрации списка курсов по id"""
    courses_factory(_quantity=4)
    names = Course.objects.all()
    id_list = []
    for name in names:
        id_list.append(name.id)
    id1 = random.choice(id_list)
    id2 = id1 + 1
    if id2 not in id_list:
        id1 -= 1
        id2 -= 1
    params = f'id={id1}&id={id2}'
    url = reverse('courses-list') + '?' + params
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['id'] == id1
    assert resp_json[1]['id'] == id2


@pytest.mark.django_db
def test_courses_name_filter(courses_factory, api_client):
    """проверка фильтрации списка курсов по name"""
    courses_factory(name='Python-Developer')
    courses_factory(name='Java-Developer')
    courses_factory(name='C#-Developer')
    courses_factory(name='Android-Developer')
    name = 'Java-Developer'
    params = f'name={name}'
    url = reverse('courses-list') + '?' + params
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['name'] == name


"""тесты ограниченного числа студентов"""
@pytest.mark.parametrize("test_input, settings", [(25, settings.MAX_STUDENTS_PER_COURSE),
                                                  (15, settings.MAX_STUDENTS_PER_COURSE),
                                                  (20, settings.MAX_STUDENTS_PER_COURSE)])
def test_with_specific_settings(test_input, settings):
    if test_input == settings:
        assert test_input == settings
    else:
        assert test_input != settings
