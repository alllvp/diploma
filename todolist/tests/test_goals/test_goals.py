import json

import pytest
from django.urls import reverse
from datetime import datetime
from rest_framework import status
from goals.models import Goal


@pytest.mark.django_db
def test_create_board(auth_client):
    url = reverse('create_board')
    payload = {
        'title': 'New Board',
    }
    response = auth_client.post(
        path=url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']


@pytest.mark.django_db
def test_create_category(auth_client, board):
    url = reverse('create_category')
    payload = {
        'board': board.pk,
        'title': 'New Category',
    }
    response = auth_client.post(
        path=url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']


@pytest.mark.django_db
def test_create_goal(auth_client, goal__category):
    url = reverse('create_goal')
    test_date = str(datetime.now().date())
    payload = {
        'title': 'New Goal',
        'category': goal__category.pk,
        'description': 'Description of New Goal',
        'due_date': test_date,
    }
    response = auth_client.post(
        path=url,
        data=payload,
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']


@pytest.mark.django_db
def test_list_boards(auth_client):

    url = reverse('list_boards')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_categories(auth_client):

    url = reverse('list_categories')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_goals(auth_client):

    url = reverse('list_goals')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_goal(auth_client, goal):

    url = reverse('retrieve_goal', kwargs={'pk': goal.pk})
    response = auth_client.get(url)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    # assert response.json()['pk'] == goal.pk
