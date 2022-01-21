from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import UsernameList, UsernameFriendList, CreateProfile, accept_req, cancel_req, del_friend, reject_req, send_req, send_message, messages

urlpatterns = [
    path('<username>/', UsernameList.as_view()),
    path('<username>/friends', UsernameFriendList.as_view()),
    path('<username>/create', CreateProfile.as_view()),
    path('<username>/send_req/', send_req.as_view()),
    path('<username>/cancel_req/', cancel_req.as_view()),
    path('<username>/accept_req/', accept_req.as_view()),
    path('<username>/reject_req/', reject_req.as_view()),
    path('<username>/del_friend/', del_friend.as_view()),
    path('<username>/dialog/send_message/', send_message),
    path('<username>/dialog/', messages.as_view()),
]