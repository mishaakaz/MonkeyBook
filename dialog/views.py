from django.views.generic import ListView
from django.shortcuts import render
from feed.models import Dialog
from django.db.models import Q


def get(request):
    dialogs = Dialog.objects.filter(Q(member1=request.user) | Q(member2 = request.user))
    
    return render(
        request,
        'dialogs_view.html',
        context={'dialogs': dialogs,
        
        }, 
    )
