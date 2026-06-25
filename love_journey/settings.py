"""
Django settings for love_journey project.
"""

from pathlib import Path
from urllib.parse import urlparse

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-l25xd%p%ta(g6(du9a-g227c!6p0g-xrcd&4w%gnzh!5&=bc6r')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1,0.0.0.0,.onrender.com,*.onrender.com,jolanda-tinglier-liana.ngrok-free.dev,*.ngrok-free.dev,*.ngrok-free.app',
    cast=Csv(),
)
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://localhost,https://127.0.0.1,https://jolanda-tinglier-liana.ngrok-free.dev,https://*.onrender.com',
    cast=Csv(),
)
SUPABASE_URL = config('SUPABASE_URL', default='').strip()
SUPABASE_ANON_KEY = config('SUPABASE_ANON_KEY', default='').strip()
if SUPABASE_URL:
    supabase_host = urlparse(SUPABASE_URL).netloc
    if supabase_host and supabase_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS = list(ALLOWED_HOSTS) + [supabase_host]
    if SUPABASE_URL not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS = list(CSRF_TRUSTED_ORIGINS) + [SUPABASE_URL]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'accounts',
    'dashboard',
    'memories',
    'timeline',
    'notes',
    'goals',
    'countdowns',
    'checkins',
    'reminders',
    'private_messages',
    'voice_messages',
    'playlists',
    'stats',
    'notifications',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'love_journey.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'love_journey.wsgi.application'

DATABASE_URL = config('DATABASE_URL', default='').strip() or config('SUPABASE_DB_URL', default='').strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if DATABASE_URL:
    try:
        parsed = urlparse(DATABASE_URL)
    except ValueError:
        parsed = None

    if parsed and parsed.scheme.startswith('postgres'):
        try:
            port = parsed.port
        except ValueError:
            port = config('SUPABASE_DB_PORT', default='5432')

        try:
            DATABASES['default'] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': parsed.path.lstrip('/') or config('SUPABASE_DB_NAME', default='postgres'),
                'USER': parsed.username or config('SUPABASE_DB_USER', default='postgres'),
                'PASSWORD': parsed.password or config('SUPABASE_DB_PASSWORD', default='postgres'),
                'HOST': parsed.hostname or config('SUPABASE_DB_HOST', default='localhost'),
                'PORT': str(port or config('SUPABASE_DB_PORT', default='5432')),
                'OPTIONS': {'sslmode': 'require'},
            }
        except ValueError:
            DATABASES['default'] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('SUPABASE_DB_NAME', default='postgres'),
                'USER': config('SUPABASE_DB_USER', default='postgres'),
                'PASSWORD': config('SUPABASE_DB_PASSWORD', default='postgres'),
                'HOST': config('SUPABASE_DB_HOST', default='localhost'),
                'PORT': config('SUPABASE_DB_PORT', default='5432'),
                'OPTIONS': {'sslmode': 'require'},
            }
elif config('SUPABASE_DB_HOST', default='').strip():
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('SUPABASE_DB_NAME', default='postgres'),
        'USER': config('SUPABASE_DB_USER', default='postgres'),
        'PASSWORD': config('SUPABASE_DB_PASSWORD', default='postgres'),
        'HOST': config('SUPABASE_DB_HOST', default='localhost'),
        'PORT': config('SUPABASE_DB_PORT', default='5432'),
        'OPTIONS': {'sslmode': 'require'},
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'home'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
