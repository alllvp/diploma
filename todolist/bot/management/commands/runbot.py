from datetime import datetime
from django.core.management.base import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from django.conf import settings
from django.utils.crypto import get_random_string


class TgState:
    """
    Determine states of telegram bot
    """
    DEFAULT = 0
    CATEGORY_CHOOSING = 1
    GOAL_CREATING = 2

    def __init__(self, state, category_id=None):
        self._state = state
        self._category_id = category_id

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, new_category_id):
        self._category_id = new_category_id


STATE = TgState(state=TgState.DEFAULT)


class Command(BaseCommand):
    help = 'Runs telegram bot'
    tg_client = TgClient(settings.TG_BOT_API_TOKEN)

    @staticmethod
    def get_ver_code(length: int = 10) -> str:
        """
        Generate random string with specified length
        """
        return get_random_string(length)

    def choose_category(self, msg: Message, tg_user: TgUser):
        """
        Choosing category for new goal
        """
        goal_categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False,
        )
        goal_categories_str = '\n'.join(['- ' + goal.title for goal in goal_categories])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Choose category: \n {goal_categories_str}'
        )
        STATE.state = TgState.CATEGORY_CHOOSING

    def check_category(self, msg: Message):
        """
        Checking if specified category exists
        """
        category = GoalCategory.objects.filter(title=msg.text).first()
        if category:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Enter goal's capture"
            )
            STATE.category_id = category.id
            STATE.state = TgState.GOAL_CREATING
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Category "{msg.text}" does not exist'
            )

    def create_goal(self, msg: Message, tg_user: TgUser):
        """
        Create new goal with specified category
        """
        category = GoalCategory.objects.get(pk=STATE.category_id)
        goal = Goal.objects.create(
            title=msg.text,
            user=tg_user.user,
            category=category,
            due_date=datetime.now().date(),
        )
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Goal "{goal.title}" created!'
        )
        STATE.state = TgState.DEFAULT

    def get_goals(self, msg: Message, tg_user: TgUser):
        """
        Get list of user's goals
        """
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user,
        ).exclude(status=Goal.Status.archived)
        goals_str = '\n'.join([goal.title for goal in goals])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Your goals:\n{goals_str}'
        )

    def cancel_operation(self, msg: Message):
        """
        Cancel all previous commands
        """
        STATE.state = TgState.DEFAULT
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Operation canceled',
        )

    def handle_message(self, msg: Message):
        """
        Processing of user's message
        """
        try:
            tg_user, created = TgUser.objects.get_or_create(
                tg_user_id=msg.msg_from.id,
                tg_chat_id=msg.chat.id,
            )
        except Exception as e:
            return e
        if created:
            tg_user.verification_code = self.get_ver_code(10)
            tg_user.save()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Please, confirm your account. "
                     f"Enter code on WEB site for verification: {tg_user.verification_code}"
            )
        if msg.text == '/goals':
            self.get_goals(msg, tg_user)
        elif msg.text == '/create':
            self.choose_category(msg, tg_user)
        elif msg.text == '/cancel':
            self.cancel_operation(msg)
        elif STATE.state == TgState.CATEGORY_CHOOSING:
            self.check_category(msg)
        elif STATE.state == TgState.GOAL_CREATING:
            self.create_goal(msg, tg_user)
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Unknown command: {msg.text}',
            )

    def handle(self, *args, **options):
        """
        Endless receiving messages from the telegram user
        """
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if hasattr(item, 'message'):
                    self.handle_message(item.message)
