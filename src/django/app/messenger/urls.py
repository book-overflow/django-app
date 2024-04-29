from django.urls import path
from . import views
from .views import all_conversations, start_conversation

urlpatterns = [
    path(
        "conversation/start/<int:user_id>/",
        views.start_conversation,
        name="start_conversation",
    ),
    path(
        "conversation/<int:conversation_id>/",
        views.view_conversation,
        name="view_conversation",
    ),
    path(
        "conversation/<int:conversation_id>/send/",
        views.send_message,
        name="send_message",
    ),
    path("messages/", all_conversations, name="all_conversations"),
    path("messages/start/", start_conversation, name="start_conversation"),
]
