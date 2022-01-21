from msilib.schema import Dialog
from django.contrib import admin
from .models import Like, Profile, Note, Friend, FriendRequest, Message, Dialog

admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(Note)
admin.site.register(Like)

admin.site.register(Dialog)
admin.site.register(Message)