from rest_framework import serializers

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    """
    Telegram User
    """
    class Meta:
        model = TgUser
        fields = ('verification_code',)
