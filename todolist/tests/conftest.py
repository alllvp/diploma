from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import factories
from pytest_factoryboy import register

USER_MODEL = get_user_model()
register(factories.GoalFactory)
register(factories.BoardFactory)
register(factories.UserFactory)
register(factories.CategoryFactory)
register(factories.BoardParticipantFactory)
register(factories.GoalCommentFactory)
register(factories.TuserFactory)


@pytest.fixture
def auth_client(db, user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture()
def boards():
    return factories.BoardFactory.create_batch(5)


@pytest.fixture()
def board():
    return factories.BoardFactory.create()


@pytest.fixture()
def boards_with_participants(user, boards):
    for item in boards:
        factories.BoardParticipantFactory.create(
            board=item,
            user=user,
        )
    return boards


@pytest.fixture()
def board_with_participant(user, board):
    factories.BoardParticipantFactory.create(
        board=board,
        user=user,
    )
    return board


@pytest.fixture()
def category(board_with_participant, user):
    return factories.CategoryFactory.create(
        board=board_with_participant,
        user=user
    )


@pytest.fixture
def goal(category, user):
    test_date = datetime.now().date()
    return factories.GoalFactory.create(
        title='New Goal',
        category=category,
        description='Description of New Goal',
        due_date=test_date,
        user=user,
    )


@pytest.fixture
def goal_comment(goal, user):
    return factories.GoalCommentFactory.create(
        text='test_comment',
        goal=goal,
        user=user,
    )


