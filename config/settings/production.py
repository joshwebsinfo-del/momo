"""
Love Journey — Production Settings
"""
from .base import *

DEBUG = False

# Security hardening
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Trust Cloudflare / Railway proxy
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins (set your domain)
CSRF_TRUSTED_ORIGINS = [
    'https://lovejourney.app',
    'https://www.lovejourney.app',
]

# Flag to optionally skip database connections (use in-memory SQLite)
SKIP_DB = config('SKIP_DB', default=False, cast=bool)

if SKIP_DB:
    # Use an in-memory SQLite database – Django will operate without a real DB.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    # Use a robust database configuration that safely handles malformed DATABASE_URL values.
    DATABASES = {'default': get_database_config()}
