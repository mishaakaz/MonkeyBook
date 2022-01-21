from django import forms
from feed.models import Message

class TextMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['chat', 'author', 'message']
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['chat'].widget = forms.HiddenInput()
