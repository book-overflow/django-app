from django.shortcuts import redirect, render
from .models import Conversation
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from shared.models import Student
from .models import Conversation


def start_conversation(request, user_id):
    # Assume `user_id` is the ID of the seller
    other_user = get_user_model().objects.get(pk=user_id)
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    return redirect("view_conversation", conversation_id=conversation.pk)


from .forms import (
    MessageForm,
)  # You'll need to create this form based on the Message model


def send_message(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect(
                "view_conversation", conversation_id=conversation_id
            )  # Redirect to the conversation view
    else:
        form = MessageForm()
    return render(
        request, "send_message.html", {"form": form, "conversation": conversation}
    )


def view_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    other_users = conversation.participants.exclude(id=request.user.id)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect("view_conversation", conversation_id=conversation_id)
    else:
        form = MessageForm()

    messages = conversation.messages.all().order_by("timestamp")
    return render(
        request,
        "view_conversation.html",
        {
            "conversation": conversation,
            "messages": messages,
            "form": form,
            "other_users": other_users,
        },
    )


def all_conversations(request):
    # Fetch all students except the logged-in user
    users = Student.objects.exclude(id=request.user.id)
    # Fetch all conversations where the current user is a participant
    conversations = Conversation.objects.filter(participants=request.user)
    return render(
        request,
        "all_conversations.html",
        {"conversations": conversations, "users": users},
    )


def start_conversation(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        other_user = get_user_model().objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        return redirect("view_conversation", conversation_id=conversation.id)
    return redirect("all_conversations")
