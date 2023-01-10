from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import factories

USER_MODEL = get_user_model()


@pytest.fixture
def test_user(db):
    user = USER_MODEL.objects.create(
        username='mister2',
        password='mister2mister2',
        email='mister2@test.com',
    )
    return user


@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    client.force_authenticate(test_user)
    return client


@pytest.fixture()
def board():
    return factories.BoardFactory.create()


@pytest.fixture()
def category(board, test_user):
    return factories.GoalCategoryFactory.create(board=board, user=test_user)


@pytest.fixture()
def board_participant(test_user, board):
    participant = factories.BoardParticipantFactory.create(
        board=board,
        user=test_user,
    )
    return participant


@pytest.fixture
def goal(category, test_user):
    test_date = datetime.now().date()
    return factories.GoalFactory.create(
        title='New Goal',
        category=category,
        description='Description of New Goal',
        due_date=test_date,
        user=test_user,
    )
