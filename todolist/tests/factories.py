import factory
from django.contrib.auth import get_user_model
from goals.models import GoalCategory, Board, BoardParticipant, Goal


USER_MODEL = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL
    username = factory.Faker('mister2')
    email = factory.Faker('mister2@test.com')
    password = 'mister2mister2'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal
