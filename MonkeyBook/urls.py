from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('django.contrib.auth.urls')),
    path('register/', include('login.urls')),
    path('friends/', include('friends.urls')),
    path('edit/', include('editProfile.urls')),
    path('dialog/', include('dialog.urls')),

    path('', include('feed.urls')),
    path('', include('page.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

