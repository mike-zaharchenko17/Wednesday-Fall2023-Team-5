import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Thread
from django.db.models import Q

@login_required
def threads_page(request):
    threads = (
        Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
        .prefetch_related("chat_message")
        .order_by("timestamp")
    )
    return render(request, "chat/threads.html", {"threads": threads})


@login_required
def messages_page(request, thread_id, other_user_id):
    json_data = {
        "thread_id": thread_id,
        "other_user_id": other_user_id,
        "self_user_id": request.user.id,
    }
    print(request.user.id)
    print(other_user_id)
    context = {"dump": json.dumps(json_data)}
    return render(request, "chat/message_room.html", context)
