import pytest
from django.urls import reverse
from datetime import datetime
from rest_framework import status
from goals.models import Goal


@pytest.mark.django_db
def test_create_goal(auth_client, category):
    url = reverse('create_goal')
    test_date = str(datetime.now().date())
    payload = {
        'title': 'New Goal',
        'category': category.pk,
        'description': 'Description of New Goal',
        'due_date': test_date,
    }
    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']


@pytest.mark.django_db
def test_retrieve_goal(auth_client, goal, test_user):
    url = reverse('retrieve_goal', kwargs={'pk': goal.pk})
    response = auth_client.get(path=url)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
