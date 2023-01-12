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


@pytest.fixture
def auth_client(db, user):
    client = APIClient()
    client.force_authenticate(user)
    return client

#
# @pytest.fixture
# def test_user(db):
#     user = USER_MODEL.objects.create(
#         username='mister2',
#         password='mister2mister2',
#         email='mister2@test.com',
#     )
#     return user

#
# @pytest.fixture()
# def board():
#     return factories.BoardFactory.create()
#
#
# @pytest.fixture()
# def category(board, user):
#     return factories.GoalCategoryFactory.create(board=board, user=user)
#
#
# @pytest.fixture()
# def board_participant(user, board):
#     participant = factories.BoardParticipantFactory.create(
#         board=board,
#         user=user,
#     )
#     return participant
#
#
# @pytest.fixture
# def goal(category, user):
#     test_date = datetime.now().date()
#     return factories.GoalFactory.create(
#         title='New Goal',
#         category=category,
#         description='Description of New Goal',
#         due_date=test_date,
#         user=user,
#     )
