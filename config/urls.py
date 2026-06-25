"""
Love Journey — Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Landing page
    path('', include('dashboard.urls_landing')),

    # Auth (accounts)
    path('accounts/', include('accounts.urls')),

    # Feature apps
    path('dashboard/', include('dashboard.urls')),
    path('memories/', include('memories.urls')),
    path('timeline/', include('timeline.urls')),
    path('notes/', include('notes.urls')),
    path('goals/', include('goals.urls')),
    path('countdowns/', include('countdowns.urls')),
    path('voice-messages/', include('voice_messages.urls')),
    path('playlist/', include('playlists.urls')),
    path('statistics/', include('statistics_app.urls')),
    path('notifications/', include('notifications.urls')),

    # REST API
    path('api/v1/', include('api.urls')),

    # CKEditor
    # path('ckeditor/', include('ckeditor.urls')),  # CKEditor disabled (package not installed)
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom admin branding
admin.site.site_header = '❤️ Love Journey Admin'
admin.site.site_title = 'Love Journey'
admin.site.index_title = 'Welcome, Admin'
