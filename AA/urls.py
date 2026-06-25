"""AA/urls.py – project URL configuration"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('dashboard.urls')),
    path('memories/', include('memories.urls')),
    path('timeline/', include('timeline.urls')),
    path('notes/', include('notes.urls')),
    path('goals/', include('goals.urls')),
    path('countdowns/', include('countdowns.urls')),
    path('voice-messages/', include('voice_messages.urls')),
    path('playlists/', include('playlists.urls')),
    path('statistics/', include('statistics_app.urls')),
    path('notifications/', include('notifications.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
