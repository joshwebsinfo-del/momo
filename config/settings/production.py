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
# Flag to optionally skip database connections (use in-memory SQLite)
SKIP_DB = config('SKIP_DB', default=False, cast=bool)

if SKIP_DB:
    # Use an in‑memory SQLite database – Django will operate without a real DB.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    # Ensure DATABASES uses a robust configuration. If DATABASE_URL is provided, parse it safely.
    db_url = config('DATABASE_URL', default='')
    if db_url:
        parsed_db = urllib.parse.urlparse(db_url)
        # Extract components safely; if any part is missing or malformed, fall back to Supabase settings.
        name = parsed_db.path.lstrip('/') or config('SUPABASE_DB_NAME', default='postgres')
        user = parsed_db.username or get_supabase_user()
        password = parsed_db.password or config('SUPABASE_DB_PASSWORD', default='')
        host = parsed_db.hostname or config('SUPABASE_DB_HOST', default='localhost')
        # parsed_db.port may raise ValueError if it contains non-numeric data; handle gracefully.
        try:
            port = str(parsed_db.port) if parsed_db.port else config('SUPABASE_DB_PORT', default='5432')
        except Exception:
            port = config('SUPABASE_DB_PORT', default='5432')
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
            'OPTIONS': {'sslmode': 'require'},
            'CONN_MAX_AGE': 60,
        }
    else:
        # Fallback to Supabase environment variables directly.
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('SUPABASE_DB_NAME', default='postgres') or 'postgres',
            'USER': get_supabase_user(),
            'PASSWORD': config('SUPABASE_DB_PASSWORD', default=''),
            'HOST': config('SUPABASE_DB_HOST', default='localhost'),
            'PORT': config('SUPABASE_DB_PORT', default='5432') or '5432',
            'OPTIONS': {'sslmode': 'require'},
            'CONN_MAX_AGE': 60,
        }
