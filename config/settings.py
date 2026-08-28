import os
from pathlib import Path
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
import dj_database_url

# Load environment variables
load_dotenv()


def env(key, default=''):
    """Get env var, stripping surrounding quotes that some dashboards (Railway) may include."""
    val = os.getenv(key, default)
    if val and len(val) >= 2 and ((val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'")):
        val = val[1:-1]
    return val


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY', 'django-insecure-mayank-classes-coaching-secret-key-default-2026')

DEBUG = env('DEBUG', 'True').lower() in ('true', '1', 'yes')

GEMINI_API_KEY = env('GEMINI_API_KEY', '')

ALLOWED_HOSTS = [host.strip() for host in env('ALLOWED_HOSTS', '*').split(',') if host.strip()]

CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in env(
        'CSRF_TRUSTED_ORIGINS',
        'http://127.0.0.1:8000,http://localhost:8000,https://*.railway.app,https://*.up.railway.app'
    ).split(',') if origin.strip()
]

# Support reverse proxy HTTPS headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party packages
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'anymail',
    
    # Internal project apps
    'apps.core.apps.CoreConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.academic.apps.AcademicConfig',
    'apps.lms.apps.LmsConfig',
    'apps.assessments.apps.AssessmentsConfig',
    'apps.operations.apps.OperationsConfig',
    'apps.portal.apps.PortalConfig',
]

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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Connects to PostgreSQL if DATABASE_URL is set (e.g. Railway), otherwise falls back to local SQLite
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ─── Email Configuration ─────────────────────────────────────────────────────
# Railway blocks outbound SMTP (ports 465/587). Use SendGrid API (HTTPS port 443) in production.
# On localhost, falls back to Gmail SMTP automatically.

SENDGRID_API_KEY = env('SENDGRID_API_KEY', '')

if SENDGRID_API_KEY:
    # Production: SendGrid HTTP API — works on Railway (no SMTP port needed)
    EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
    ANYMAIL = {
        'SENDGRID_API_KEY': SENDGRID_API_KEY,
    }
    print('[EMAIL] Using SendGrid API backend (production mode)')
else:
    # Local Development: Gmail SMTP
    EMAIL_BACKEND = env('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = env('EMAIL_HOST', 'smtp.gmail.com').strip()
    EMAIL_PORT = int(env('EMAIL_PORT', '587'))

    _use_tls_env = env('EMAIL_USE_TLS', '')
    _use_ssl_env = env('EMAIL_USE_SSL', '')

    if _use_ssl_env:
        EMAIL_USE_SSL = _use_ssl_env.lower() in ('true', '1', 'yes')
        EMAIL_USE_TLS = False if EMAIL_USE_SSL else (_use_tls_env.lower() in ('true', '1', 'yes') if _use_tls_env else True)
    elif EMAIL_PORT == 465:
        EMAIL_USE_SSL = True
        EMAIL_USE_TLS = False
    else:
        EMAIL_USE_SSL = False
        EMAIL_USE_TLS = _use_tls_env.lower() in ('true', '1', 'yes') if _use_tls_env else True

    EMAIL_HOST_USER = env('EMAIL_HOST_USER', '').strip()
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', '').strip()
    EMAIL_TIMEOUT = int(env('EMAIL_TIMEOUT', '15'))
    print(f'[EMAIL] Using SMTP backend: {EMAIL_HOST}:{EMAIL_PORT} (local/dev mode)')

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', '').strip() or 'Mayank Classes <admissions@mayankclasses.com>'
ADMIN_EMAIL_NOTIFICATION = env('ADMIN_EMAIL_NOTIFICATION', '').strip() or env('EMAIL_HOST_USER', '')


# Production Logging Configuration (Ensures logs appear in Railway dashboard)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


