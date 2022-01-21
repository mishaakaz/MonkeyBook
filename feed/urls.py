from django.urls import path
from .views import index, NoteDetailView, LikeNote, UnlikeNote, DeleteNote, about
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', login_required(index), name='feed'),
    path('about/', about, name='about_us'),
    path('note/<int:pk>/unlike/', UnlikeNote.as_view()),
    path('note/<int:pk>/delete/', DeleteNote.as_view()),
    path('note/<int:pk>/like/<int:vote>', LikeNote.as_view()),
    path('note/<int:pk>/', NoteDetailView.as_view()),
]