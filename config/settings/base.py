"""
Love Journey — Base Django Settings
Shared across all environments.
"""

import os
from pathlib import Path
from decouple import config, Csv

# ============================================================
# Paths
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ============================================================
# Security
# ============================================================
SECRET_KEY = config('SECRET_KEY', default='insecure-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ============================================================
# Custom User Model
# ============================================================
AUTH_USER_MODEL = 'accounts.User'

# ============================================================
# Installed Apps
# ============================================================
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'ckeditor',
    'django_celery_beat',
]

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',
    'memories.apps.MemoriesConfig',
    'timeline.apps.TimelineConfig',
    'notes.apps.NotesConfig',
    'goals.apps.GoalsConfig',
    'countdowns.apps.CountdownsConfig',
    'voice_messages.apps.VoiceMessagesConfig',
    'playlists.apps.PlaylistsConfig',
    'statistics_app.apps.StatisticsAppConfig',
    'notifications.apps.NotificationsConfig',
    'api.apps.ApiConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ============================================================
# Middleware
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================
# URL Configuration
# ============================================================
ROOT_URLCONF = 'config.urls'

# ============================================================
# Templates
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notifications_processor',
            ],
        },
    },
]

# ============================================================
# WSGI / ASGI
# ============================================================
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ============================================================
# Database — Supabase PostgreSQL
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('SUPABASE_DB_NAME', default='postgres'),
        'USER': config('SUPABASE_DB_USER', default='postgres'),
        'PASSWORD': config('SUPABASE_DB_PASSWORD', default=''),
        'HOST': config('SUPABASE_DB_HOST', default='localhost'),
        'PORT': config('SUPABASE_DB_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 60,
    }
}

# Default auto field — use UUID in models explicitly
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# Auth Password Validators
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# Localisation
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================================
# Static Files
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================
# Media Files (local dev fallback — prod uses Supabase Storage)
# ============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# Supabase Storage Config
# ============================================================
SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_ANON_KEY = config('SUPABASE_ANON_KEY', default='')
SUPABASE_SERVICE_ROLE_KEY = config('SUPABASE_SERVICE_ROLE_KEY', default='')

# Storage bucket names
SUPABASE_BUCKET_MEMORIES = 'memories'
SUPABASE_BUCKET_VOICE = 'voice-notes'
SUPABASE_BUCKET_PROFILES = 'profile-pictures'

# File size limits (bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024   # 10 MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024   # 50 MB
MAX_AUDIO_SIZE = 20 * 1024 * 1024   # 20 MB

# ============================================================
# Couple Access Control
# ============================================================
ALLOWED_COUPLE_EMAILS = [
    config('ALLOWED_EMAIL_1', default=''),
    config('ALLOWED_EMAIL_2', default=''),
]
RELATIONSHIP_START_DATE = config('RELATIONSHIP_START_DATE', default='2023-01-01')

# ============================================================
# Authentication
# ============================================================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ============================================================
# Session Security
# ============================================================
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True

# ============================================================
# Django REST Framework
# ============================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
    },
}

# ============================================================
# CKEditor (Rich Text for Love Notes)
# ============================================================
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['TextColor', 'BGColor'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['BulletedList', 'NumberedList'],
            ['Link', 'Unlink'],
            ['Undo', 'Redo'],
        ],
        'height': 300,
        'width': '100%',
    }
}

# ============================================================
# Celery
# ============================================================
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# ============================================================
# Email
# ============================================================
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='noreply@lovejourney.app')

# ============================================================
# CORS
# ============================================================
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
CORS_ALLOW_CREDENTIALS = True

# ============================================================
# Logging
# ============================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
