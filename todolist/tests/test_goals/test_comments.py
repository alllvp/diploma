import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_retrieve_comment(auth_client, goal_comment):

    url = reverse('retrieve_comment', kwargs={'pk': goal_comment.pk})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == goal_comment.pk


@pytest.mark.django_db
def test_list_comments(auth_client):

    url = reverse('list_comments')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_comment(auth_client, goal):
    url = reverse('create_comment')
    payload = {
        'text': 'test_comment',
        'goal': goal.pk,
    }
    response = auth_client.post(
        path=url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['text'] == payload['text']


@pytest.mark.django_db
def test_update_comment(auth_client, goal, goal_comment):
    url = reverse('retrieve_comment', kwargs={'pk': goal_comment.pk})
    payload = {
        'text': 'test_comment',
        'goal': goal.pk,
    }
    response = auth_client.put(
        path=url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['text'] == payload['text']
