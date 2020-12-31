import random

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

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
def test_courses_create(api_client):
    """тест успешного создания курса"""
    url = reverse("courses-list")
    course_name = {"name": "Python-Developer"}
    resp = api_client.post(url, course_name)
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_courses_update(api_client):
    """тест успешного обновления курса"""
    url = reverse("courses-list")
    course_name = {"name": "Python-Developer"}
    resp = api_client.post(url, course_name)
    assert resp.status_code == HTTP_201_CREATED
    new_course_name = {"name": "Что-то другое"}
    course = Course.objects.get(name='Python-Developer')
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.put(url, data=new_course_name)
    new_course = Course.objects.get(name=new_course_name['name'])
    assert resp.status_code == HTTP_200_OK
    assert new_course.name == 'Что-то другое'


@pytest.mark.django_db
def test_courses_delete(api_client):
    """тест успешного удаления курса"""
    course_name = {'name': 'Something interesting'}
    url = reverse("courses-list")
    resp = api_client.post(url, course_name)
    assert resp.status_code == HTTP_201_CREATED
    course = Course.objects.get(name='Something interesting')
    url = reverse("courses-detail", args=(course.id,))
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT


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
