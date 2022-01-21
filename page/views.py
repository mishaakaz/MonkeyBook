
from re import S
from django.shortcuts import render
from django.views.decorators.http import require_POST
from page.forms import TextMessage
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from feed.models import Dialog, FriendRequest, Message, Profile, Friend, Note, Like
from django.contrib.auth.models import User
from django.db.models import Q
from feed.forms import ImageForm
from django.http.request import HttpRequest

class UsernameList(ListView):

    model = Profile

    template_name = 'userpage.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username'])
        return self.user

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['current_user'] = self.user
        
        try:
            sending_friend_request = [FriendRequest.objects.get(receiver = self.user)]
        except FriendRequest.DoesNotExist:
            sending_friend_request = []

        applied_friend_request = []
        try:
            applied_friend_request = FriendRequest.objects.get(sender = self.user, receiver = self.request.user)
        except FriendRequest.DoesNotExist:
            applied_friend_request = []

        context['sending_friend_request'] = sending_friend_request
        context['applied_friend_request'] = applied_friend_request
        context['sub_list_count'] = len(sending_friend_request)

        form = ImageForm(self.request.POST or None, self.request.FILES or None, initial={'author': self.request.user})
        if form.is_valid():
            form.save()
            return self.redirect("/")
        context['form'] = form

        friend_List = get_friends_list(self.user)
        friend_count = len(friend_List)
        is_friend = False
        
        for i in friend_List:
            if i == self.request.user:
                is_friend = True
                break
            else: is_friend = False
        
        context['is_friend'] = is_friend
        context['friend_count'] = friend_count
        context['friend_declination'] = get_friend_declination(friend_count)

        notes = Note.objects.all().order_by('-created').filter(author = self.user)
        likes = Like.objects.filter(user = self.request.user)
        context['notes'] = notes
        context['likes'] = likes

        context['notes_declination'] = get_note_declination(notes.count())

        return context

def get_friends_list(user):

    friends_users = Friend.objects.filter(users = user)
    friends_cur_user = Friend.objects.filter(current_user = user)

    friend_list = []
    for friend in friends_users:
        friend_list.append(Friend.get_current_user(friend))

    for friend in friends_cur_user:
       friend_list.append(Friend.get_users(friend))  

    return friend_list

def get_friend_declination(friend_count):
    fch = friend_count % 10 #friend_count_helper
    friend_result = " "

    if fch == 0 or (fch >= 5 and fch <= 9) or (friend_count >= 10 and friend_count <= 20): friend_result = " друзей"
    elif fch == 1 or friend_count == 1: friend_result = " друг"
    elif fch > 1 or fch < 5 or friend_count > 1 or friend_count < 5: friend_result = " друга"

    return friend_result

#Страница друзей человека

class UsernameFriendList(ListView):
    model = Profile

    template_name = 'friends_page.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username'])
        return self.user

    def get_context_data(self, **kwargs):
        
        friend_list = get_friends_list(self.user)

        context = super().get_context_data(**kwargs)
        context['friend_list'] = friend_list
        context['current_user'] = self.user

        return context

def get_note_declination(notes_count):
    nch = notes_count % 10 #notes_count_helper
    notes_result = " "

    if nch == 0 or (nch >= 5 and nch <= 9) or (notes_count >= 10 and notes_count <= 20): notes_result = " постов"
    elif nch == 1 or notes_count == 1: notes_result = " пост"
    elif nch > 1 or nch < 5 or notes_count > 1 or notes_count < 5: notes_result = " поста"

    return notes_result

#Создание профиля
class CreateProfile(ListView):
    model = Profile

    template_name = 'like_template.html'

    def get_queryset(self):
        obj, create = Profile.objects.get_or_create(user = self.request.user)

        obj.nickname = self.request.user.username
        obj.name = 'zalupa'
        obj.save()
        
        return redirect('/', self.request.user.username, '/')
    
class send_req(ListView):
    model = FriendRequest
    template_name = 'like_template.html'

    def get_queryset(self):
        rec = get_object_or_404(User, username = self.kwargs['username'])
        try: friend1 = Friend.object.get.filter(users = self.request.user, current_user = rec)
        except: friend1 = None
        try: friend2 = Friend.object.get.filter(users= rec, current_user = self.request.user)
        except: friend2 = None

        if not friend1 and not friend2:
            obj, create = FriendRequest.objects.get_or_create(sender = self.request.user, receiver = rec)
            obj.save()

        return rec

class cancel_req(ListView):
    model = FriendRequest
    template_name = 'like_template.html'

    def get_queryset(self):
        rec = get_object_or_404(User, username = self.kwargs['username'])

        FriendRequest.objects.filter(sender = self.request.user, receiver = rec).delete()
        
        return rec

class accept_req(ListView):
    model = FriendRequest
    template_name = 'like_template.html'

    def get_queryset(self):
        rec = get_object_or_404(User, username = self.kwargs['username'])
        obj, create = Friend.objects.get_or_create(users = self.request.user, current_user = rec)
        obj.save()
        FriendRequest.objects.filter(sender = self.request.user, receiver = rec).delete()
        
        return rec

class reject_req(ListView):
    model = FriendRequest
    template_name = 'like_template.html'

    def get_queryset(self):
        rec = get_object_or_404(User, username = self.kwargs['username'])
        obj = FriendRequest.objects.filter(sender = self.request.user, receiver = rec)
        try: obj.hidden = True
        except: pass
        obj.save()
        return rec

class del_friend(ListView):
    model = FriendRequest
    template_name = 'like_template.html'

    def get_queryset(self):
        rec = get_object_or_404(User, username = self.kwargs['username'])
        Friend.objects.filter(users = self.request.user, current_user = rec).delete()
        Friend.objects.filter(users = rec, current_user = self.request.user).delete()
        return rec

class messages(ListView):
    model = Message
    template_name = 'messages.html'
    messages = []


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        cur = User.objects.get(username = self.kwargs['username'])
        messages = None
        dialog = Dialog.objects.filter(Q(member1=self.request.user) | Q(member2 = self.request.user)).filter(Q(member1=cur) | Q(member2 = cur))
        if dialog: messages = Message.objects.filter(chat = dialog[0])
        else: dialog = [Dialog.objects.create(member1 = self.request.user, member2 = cur)]
        form = TextMessage(self.request.POST or None, self.request.FILES or None, initial={'chat': dialog[0], 'author': cur})
        context['form'] = form
        context['messages'] = messages
        context['current_user'] = cur
        return context

@require_POST
def send_message(request, username):
    cur = User.objects.get(username = username)
    dialog = Dialog.objects.filter(Q(member1=request.user) | Q(member2 = request.user)).filter(Q(member1=cur) | Q(member2 = cur))
    form = TextMessage(request.POST or None, request.FILES or None, initial={'chat': dialog[0], 'author': cur})

    if form.is_valid():
        form.save()
    return redirect('/', username, '/dialog') 


