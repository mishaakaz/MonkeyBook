from django import forms
from .models import Note

class ImageForm(forms.ModelForm):
    class Meta:
        model= Note
        fields= ["author", "text", "note_image"]

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['text'].widget.attrs['rows'] = 1
        self.fields['text'].widget.attrs['placeholder'] = "Что у вас нового?"
        self.fields['note_image'].widget.attrs['class'] = 'inputfile'