from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models.fields import CharField
from django.forms.widgets import PasswordInput
from feed.models import Profile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'nickname', 'status', 'photo']

