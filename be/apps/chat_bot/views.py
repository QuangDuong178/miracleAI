from django.http import StreamingHttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat_bot.models import MasterConversation
from apps.chat_bot.serializers import MasterConversationSerializer
from apps.chat_bot.services import streaming_response
from apps.core.exceptions import ResourceNotFoundException


class ChatbotView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        data = request.data
        master_id = data.get("masterId", 1)
        history_messages = data.get("history_messages", [])

        try:
            master = MasterConversation.objects.get(id=master_id)
        except MasterConversation.DoesNotExist:
            raise ResourceNotFoundException()

        return StreamingHttpResponse(streaming_response(master=master, history_messages=history_messages),
                                     content_type="text/event-stream")


class MasterView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        master_conversations = MasterConversation.objects.all()
        serializers = MasterConversationSerializer(master_conversations, many=True, context={"request": request})
        return Response(serializers.data, status=status.HTTP_200_OK)
