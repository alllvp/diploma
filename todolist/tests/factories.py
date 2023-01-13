import factory
from django.contrib.auth import get_user_model
from goals.models import GoalCategory, Board, BoardParticipant, Goal, GoalComment
from bot.models import TgUser


USER_MODEL = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    username = 'mister2'
    email = 'mister2@test.com'
    password = 'mister2mister2'

    class Meta:
        model = USER_MODEL


class BoardFactory(factory.django.DjangoModelFactory):
    title = 'New Board'

    class Meta:
        model = Board


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


class CategoryFactory(factory.django.DjangoModelFactory):
    title = 'New Category'
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalCategory


class GoalFactory(factory.django.DjangoModelFactory):
    title = 'New Goal'
    description = 'Description of New Goal'
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    due_date = factory.Faker('date_object')

    class Meta:
        model = Goal


class GoalCommentFactory(factory.django.DjangoModelFactory):
    text = 'test comment'
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalComment


class TuserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TgUser
