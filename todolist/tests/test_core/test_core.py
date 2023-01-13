import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_signup(auth_client):
    url = reverse('signup')
    payload = {
        'username': 'mister3',
        'email': 'mister3@test.com',
        'password': 'mister3mister3',
        'password_repeat': 'mister3mister3'
    }
    response = auth_client.post(
        path=url,
        data=payload,
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['username'] == payload['username']
