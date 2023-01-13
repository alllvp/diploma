import json

import pytest
from django.urls import reverse
from datetime import datetime
from rest_framework import status


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
def test_list_categories(auth_client):

    url = reverse('list_categories')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_category(auth_client, category):

    url = reverse('retrieve_category', kwargs={'pk': category.pk})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == category.pk


@pytest.mark.django_db
def test_update_category(auth_client, category, board):
    url = reverse('retrieve_category', kwargs={'pk': category.pk})
    payload = {
        'board': board.pk,
        'title': 'New Category',
    }
    response = auth_client.put(
        path=url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['title'] == payload['title']
