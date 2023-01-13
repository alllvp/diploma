import json
import factories
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_bot_verify(auth_client, user):
    factories.TuserFactory.create(
        tg_chat_id=123445,
        tg_user_id=124315315,
        tg_username='testuser',
        user=user,
        verification_code='correct'
    )
    url = reverse('bot_verify')
    payload1 = {
        'verification_code': 'correct'
    }
    payload2 = {
        'verification_code': 'incorrect'
    }

    response1 = auth_client.patch(
        path=url,
        data=json.dumps(payload1),
        content_type='application/json',
    )
    response2 = auth_client.patch(
        path=url,
        data=json.dumps(payload2),
        content_type='application/json',
    )

    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_400_BAD_REQUEST

