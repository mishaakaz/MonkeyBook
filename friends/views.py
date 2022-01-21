from django.shortcuts import render, redirect
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from feed.models import FriendRequest

from django.views.generic import ListView
from feed.models import Profile
from feed.models import Friend
from django.contrib.auth.models import User

def friend_request(request, pk):
    sender = request.user
    recipient = User.objects.get(id=pk)
    model = FriendRequest.objects.get_or_create(sender=request.user, receivers=recipient)
    return redirect('/')

def delete_request(request, operation, pk):
    client1 = User.objects.get(id=pk)
    print(client1)
    if operation == 'Sender_deleting':
        model1 = FriendRequest.objects.get(sender=request.user, receivers=client1)
        model1.delete()
    elif operation == 'Receiver_deleting':
        model2 = FriendRequest.objects.get(sender=client1, receivers=request.user)
        model2.delete()
        return redirect('/')
    return redirect('/')

def add_or_remove_friend(request, operation, pk):
    new_friend = User.objects.get(id=pk)
    if operation == 'add':
        fq = FriendRequest.objects.get(sender=new_friend, receivers=request.user)
        Friend.make_friend(request.user, new_friend)
        Friend.make_friend(new_friend, request.user)
        fq.delete()
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)
        Friend.lose_friend(new_friend, request.user)
    return redirect('/')

def index(request):

    friend_list = get_friends_list(request)
    friend_list_count = len(friend_list)

    return render(
        request,
        'friends_page.html',
        context={'current_user': request.user,
            'friend_list': friend_list,
            'friend_list_count': friend_list_count,}
    )

def get_friends_list(request):

   friends_users = Friend.objects.filter(users = request.user)
   friends_cur_user = Friend.objects.filter(current_user = request.user)

   friend_list = []
   for friend in friends_users:
       friend_list.append(Friend.get_current_user(friend))

   for friend in friends_cur_user:
       friend_list.append(Friend.get_users(friend))  

   return friend_list

def subscribers(request):

    accept_list = []
    for x in FriendRequest.objects.filter(receiver = request.user):
        accept_list.append(x.sender)
    accept_list_count = len(accept_list)    

    return render(
        request,
        'receiver_page.html',
        context={'current_user': request.user,
            'friend_list': accept_list,
            'friend_list_count': accept_list_count,}
    )

def subscriptions(request):

    sender_list = []
    for x in FriendRequest.objects.filter(sender = request.user):
        sender_list.append(x.receiver)
    sender_list_count = len(sender_list)

    return render(
        request,
        'sender_page.html',
        context={'current_user': request.user,
            'friend_list': sender_list,
            'friend_list_count': sender_list_count,}
    )
