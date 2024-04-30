from django.shortcuts import redirect, render
from .models import Conversation
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from shared.models import Student
from .models import Conversation, Message
from django.db.models import Q


def start_conversation(request, user_id):
    if request.method == "POST":
        other_user = get_user_model().objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        conversation.save()
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


# def view_conversation(request, conversation_id):
#     conversation = get_object_or_404(Conversation, pk=conversation_id)
#     other_users = conversation.participants.exclude(
#         id=request.user.id
#     )  # Get the other participant

#     if request.method == "POST":
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.conversation = conversation
#             message.save()
#             return redirect("view_conversation", conversation_id=conversation_id)
#     else:
#         form = MessageForm()

#     messages = conversation.messages.all().order_by("timestamp")
#     return render(
#         request,
#         "view_conversation.html",
#         {
#             "conversation": conversation,
#             "messages": messages,
#             "form": form,
#             "other_users": other_users,
#         },
#     )

from django.http import HttpResponse


def view_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    # If current user is not a participant
    if request.user not in conversation.participants.all():
        return HttpResponse("No conversation found, something is wrong.")
    else: 
        # Ensure we are fetching the other user correctly
        users = conversation.participants.exclude(email="admin@admin.com")
        other_user = users.exclude(id=request.user.id)[0]
        other_conversations = Conversation.objects.filter(participants=request.user)
        other_users = []
        for c in other_conversations:
            c_messages = c.messages.all()
            if c_messages:
                last_message = c_messages.order_by("-timestamp")[0]
                for participant in c.participants.all().exclude(email=request.user.email):
                    student = Student.objects.get(email=participant)
                    other_users.append({
                        'id': c.pk, 
                        'student': student, 
                        'last_message': last_message
                    })
        if not users.exists():
            return HttpResponse("No other participants found, something is wrong.")

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

        other_users = sorted(other_users, key=lambda d:d['last_message'].timestamp, reverse=True)

        return render(request, "view_conversation.html", {
            "conversation": conversation,
            "msgs": messages, 
            "form": form,
            "other_user": other_user,
            "other_users": other_users,
        })


def all_conversations(request):
    # Fetch all conversations where the current user is a participant
    conversations = Conversation.objects.filter(participants=request.user)
    chats = []
    for c in conversations:
        messages = c.messages.all()
        if messages:
            last_message = messages.order_by("-timestamp")[0]
            for participant in c.participants.all().exclude(email=request.user.email):
                student = Student.objects.get(email=participant)
                chats.append({
                    'conversation': c, 
                    'student': student, 
                    'last_message': last_message,
                })

    # Sort the chats by last message's timestamp
    latest_chat, other_chats = None, None
    if len(chats) >= 2:
        chats = sorted(chats, key=lambda d:d['last_message'].timestamp, reverse=True)
        latest_chat = chats[0]
        other_chats = chats[1:]
    elif len(chats) == 1:
        chats = sorted(chats, key=lambda d:d['last_message'].timestamp, reverse=True)
        latest_chat = chats[0]

    return render(request, "all_conversations.html", 
                  {"latest_chat": latest_chat, "other_chats": other_chats})


def start_conversation(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        other_user = get_user_model().objects.get(pk=user_id)
        # Do not create new conversation if exists
        if Conversation.objects.filter(participants=request.user).filter(participants=other_user).exists():
            conversation = Conversation.objects.filter(participants=request.user,).filter(participants=other_user)[0]
        else:        
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, other_user)
        return redirect("view_conversation", conversation_id=conversation.pk)
    return redirect("all_conversations")
