from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import get

urlpatterns = [
    path('', login_required(get)),

]