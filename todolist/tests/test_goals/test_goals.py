import json

import pytest
from django.urls import reverse
from datetime import datetime
from rest_framework import status


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
def test_list_goals(auth_client):

    url = reverse('list_goals')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_goal(auth_client, goal):

    url = reverse('retrieve_goal', kwargs={'pk': goal.pk})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == goal.pk


@pytest.mark.django_db
def test_update_goal(auth_client, goal, goal__category):
    test_date = str(datetime.now().date())
    url = reverse('retrieve_goal', kwargs={'pk': goal.pk})
    response = auth_client.put(
        url,
        data={
            'title': 'test',
            'category': goal__category.pk,
            'description': 'test_descr',
            'due_date': test_date
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'test'



