"""
URL configuration for love_journey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('memories/', include('memories.urls')),
    path('timeline/', include('timeline.urls')),
    path('notes/', include('notes.urls')),
    path('goals/', include('goals.urls')),
    path('countdowns/', include('countdowns.urls')),
    path('voice/', include('voice_messages.urls')),
    path('playlists/', include('playlists.urls')),
    path('stats/', include('stats.urls')),
    path('checkins/', include('checkins.urls')),
    path('reminders/', include('reminders.urls')),
    path('messages/', include('private_messages.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
