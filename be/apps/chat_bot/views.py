from django.http import StreamingHttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat_bot.models import Bot
from apps.chat_bot.serializers import BotSerializer
from apps.chat_bot.services import streaming_response
from apps.core.exceptions import ResourceNotFoundException


class ChatbotView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        data = request.data
        history_messages = data.get("history_messages", [])

        try:
            bot = Bot.objects.get(id=1)
        except Bot.DoesNotExist:
            raise ResourceNotFoundException()

        return StreamingHttpResponse(streaming_response(bot=bot, history_messages=history_messages),
                                     content_type="text/event-stream")


class MasterView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        serializers = BotSerializer(bots, many=True, context={"request": request})
        return Response(serializers.data, status=status.HTTP_200_OK)
