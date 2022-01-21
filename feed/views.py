import profile
from django.http import request
from django.shortcuts import redirect, render
from .models import Note, Like, Profile
from .forms import ImageForm
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from page.views import get_friends_list

def index(request):
    friends = get_friends_list(request.user)
    
    notes = Note.objects.all().order_by('-created')

    notes.reverse()
    likes = Like.objects.filter(user = request.user)

    form = ImageForm(request.POST or None, request.FILES or None, initial={'author': request.user})
    if form.is_valid():
        form.save()
        return redirect("/")

    return render(
        request,
        'index.html',
        context={"notes": notes,
        'form': form,
        'likes': likes}, 
    )

#Отдельный пост
class NoteDetailView(ListView):
    model = Note

    template_name = 'note_page.html'

    def get_queryset(self):
        self.note = get_object_or_404(Note, id = self.kwargs['pk'])
        return self.note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note'] = self.note

        return context

#Лайк поста
class LikeNote(ListView):
    model = Like

    template_name = 'like_template.html'

    def get_queryset(self):
        self.note = get_object_or_404(Note, id = self.kwargs['pk'])

        obj, create = Like.objects.get_or_create(user = self.request.user, note = self.note)
        obj.vote = self.kwargs['vote']
        obj.save()

        return self.note

#Отмена лайка поста
class UnlikeNote(ListView):
    model = Like

    template_name = 'like_template.html'

    def get_queryset(self):
        self.note = get_object_or_404(Note, id = self.kwargs['pk'])

        Like.objects.filter(user = self.request.user, note = self.note).delete()

        return self.note

#Удаление поста
class DeleteNote(ListView):
    model = Note

    template_name = 'like_template.html'

    def get(self, *args, **kwargs):
        self.note = get_object_or_404(Note, id = self.kwargs['pk'])

        self.note.delete()

        return redirect('/')

def about(request):
    
    return render(
        request,
        'about.html', 
    )