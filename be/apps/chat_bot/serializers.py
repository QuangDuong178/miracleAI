from rest_framework import serializers

from apps.chat_bot.models import Bot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ("storage_vector_name","vector_config_name")
