from django.http import request
from django.shortcuts import render
from feed.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate

from django.contrib.auth import views as auth_views

class MyLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile_id = Profile.objects.get(user = request.user)

        context.update({
            'profile': profile_id,
        })
        return context

def register(request):
    if request.method == 'POST':

        form_reg = UserCreationForm(request.POST)

        if form_reg.is_valid():
            form_reg.save()
            username = form_reg.cleaned_data.get('username')
            password = form_reg.cleaned_data.get('password1')
            user =  authenticate(request, username = username, password = password)

            if user:
                obj, create = Profile.objects.get_or_create(user = user)

                obj.nickname = user.username
                obj.name = user.username
                obj.save()

                login(request, user)
                return redirect("/")
    else:
        form_reg = UserCreationForm()
        return render(request, 'login.html', {'form_reg' : form_reg,})