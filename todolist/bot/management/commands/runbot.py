from datetime import datetime
from django.core.management.base import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from django.conf import settings
from django.utils.crypto import get_random_string


class TgState:
    DEFAULT = 0
    CATEGORY_CHOOSING = 1
    GOAL_CREATING = 2

    def __init__(self, state, category_id=None):
        self.state = state
        self.category_id = category_id

    def set_state(self, state):
        self.state = state

    def set_category_id(self, category_id):
        self.category_id = category_id


STATE = TgState(state=TgState.DEFAULT)


class Command(BaseCommand):
    help = 'Runs telegram bot'
    tg_client = TgClient(token=settings.TG_BOT_API_TOKEN)

    def choose_category(self, msg: Message, tg_user: TgUser):
        goal_categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False,
        )
        goal_categories_str = '\n'.join(['- ' + goal.title for goal in goal_categories])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Choose category: \n {goal_categories_str}'
        )
        STATE.set_state(TgState.CATEGORY_CHOOSING)

    def check_category(self, msg: Message):
        category = GoalCategory.objects.filter(title=msg.text).first()
        if category:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Enter goal's capture"
            )
            STATE.set_category_id(category.id)
            STATE.set_state(TgState.GOAL_CREATING)
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Category "{msg.text}" does not exist'
            )

    def create_goal(self, msg: Message, tg_user: TgUser):
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
        STATE.set_state(TgState.DEFAULT)

    def get_goals(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user,
        ).exclude(status=Goal.Status.archived)
        goals_str = '\n'.join([goal.title for goal in goals])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Your goals:\n{goals_str}'
        )

    def cancel_operation(self, msg: Message):
        STATE.set_state(TgState.DEFAULT)
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Operation canceled',
        )

    def handle_message(self, msg: Message):
        try:
            tg_user, created = TgUser.objects.get_or_create(
                tg_user_id=msg.msg_from.id,
                tg_chat_id=msg.chat.id,
            )
        except Exception as e:
            return e
        if created:
            tg_user.verification_code = get_random_string(10)
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
        offset = 0
        while True:
            try:
                res = self.tg_client.get_updates(offset=offset)
            except Exception as e:
                print(e)
                offset += 1
                continue

            for item in res.result:
                offset = item.update_id + 1
                if hasattr(item, 'message'):
                    self.handle_message(item.message)
