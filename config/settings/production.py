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

import urllib.parse
db_url = config('DATABASE_URL', default='')
if db_url:
    parsed_db = urllib.parse.urlparse(db_url)
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed_db.path.lstrip('/') or 'postgres',
        'USER': parsed_db.username,
        'PASSWORD': parsed_db.password,
        'HOST': parsed_db.hostname,
        'PORT': parsed_db.port or '6543',
        'OPTIONS': {'sslmode': 'require'},
        'CONN_MAX_AGE': 60,
    }
