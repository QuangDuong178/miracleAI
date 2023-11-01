from django.urls import path

from apps.chat_bot.views import ChatbotView, MasterView

urlpatterns = [
    path("send-message/", ChatbotView.as_view(), name="send_message_to_bot"),
    path("masters/", MasterView.as_view(), name="master_list"),
]
