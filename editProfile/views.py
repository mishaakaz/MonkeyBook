from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from .forms import EditProfileForm, PasswordChangeForm
from feed.models import Profile
from django.contrib.auth.models import User

def change_profile(request):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        form = EditProfileForm(request.POST or None, request.FILES or None, instance = user_profile)

        if form.is_valid():
            form.save()
            user_profile = Profile.objects.get(user=request.user)

    if request.method == 'GET':
        user_profile = Profile.objects.get(user=request.user)
        form = EditProfileForm(instance=user_profile)

    return render(
        request, 
        'edit_profile.html', 
        context = {'user_profile' : user_profile, 
        'form' : form},
        )



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('/', request.user)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_pass.html', {
        'form': form
    })