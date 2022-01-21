from django.urls import path
from .views import index, subscribers, subscriptions
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    path('', login_required(index), name='friends'),
    path('receiver', login_required(subscribers)),
    path('sender', login_required(subscriptions)),
]