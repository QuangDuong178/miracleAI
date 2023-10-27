from rest_framework import serializers

from apps.chat_bot.models import MasterConversation


class MasterConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterConversation
        fields = ("id", "name", "description", "avatar")
