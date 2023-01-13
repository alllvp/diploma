import json

import pytest
from django.urls import reverse
from rest_framework import status
import factories

from goals.serializers import BoardListSerializer


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
def test_list_boards(auth_client):
    url = reverse('list_boards')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_boards_2(auth_client, user):
    url = reverse('list_boards')
    boards = factories.BoardFactory.create_batch(2)
    for board in boards:
        factories.BoardParticipantFactory.create(board=board, user=user)
    response = auth_client.get(f'{url}?limit=2')

    expected_response = {
        'count': 2,
        'next': None,
        'previous': None,
        'results': BoardListSerializer(instance=boards, many=True).data
    }
    assert response.data['count'] == 2
    assert response.data == expected_response


@pytest.mark.django_db
def test_list_boards_3(auth_client, boards_with_participants):
    url = reverse('list_boards')
    response = auth_client.get(f'{url}?limit=5')

    expected_response = {
        'count': 5,
        'next': None,
        'previous': None,
        'results': BoardListSerializer(instance=boards_with_participants, many=True).data
    }
    assert response.data['count'] == 5
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve_board(auth_client, board_with_participant):

    url = reverse('retrieve_board', kwargs={'pk': board_with_participant.pk})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == board_with_participant.pk


@pytest.mark.django_db
def test_update_board(auth_client, user, board_with_participant):
    url = reverse('retrieve_board', kwargs={'pk': board_with_participant.pk})
    payload = {
        'title': 'test',
        'participants': []
    }
    response = auth_client.put(
        path=url,
        data=json.dumps(payload),
        content_type='application/json',
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['title'] == payload['title']
