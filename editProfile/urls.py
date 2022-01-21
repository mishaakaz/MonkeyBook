from django.urls import path
from django.contrib.auth.decorators import login_required
from editProfile.views import change_profile, change_password


urlpatterns = [
    path('', login_required(change_profile), name='edit'),
    path('profile/', login_required(change_profile), name='edit_profile'),
    path('password/', login_required(change_password), name='edit_password'),
]
