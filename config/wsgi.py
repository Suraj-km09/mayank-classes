"""
WSGI config for Mayank Classes platform.
Compatible with PythonAnywhere, Gunicorn, uWSGI, and Heroku.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Startup SMTP diagnostics — visible in Railway/Gunicorn logs on every boot
try:
    from django.conf import settings
    has_password = bool(settings.EMAIL_HOST_PASSWORD)
    print("=" * 60)
    print("[STARTUP] SMTP Email Configuration Summary:")
    print(f"  EMAIL_HOST:     {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT:     {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS:  {getattr(settings, 'EMAIL_USE_TLS', False)}")
    print(f"  EMAIL_USE_SSL:  {getattr(settings, 'EMAIL_USE_SSL', False)}")
    print(f"  EMAIL_USER:     {settings.EMAIL_HOST_USER or '[NOT SET]'}")
    print(f"  EMAIL_PASSWORD: {'SET (' + str(len(settings.EMAIL_HOST_PASSWORD)) + ' chars)' if has_password else '[NOT SET - EMAILS WILL FAIL!]'}")
    print(f"  DEFAULT_FROM:   {settings.DEFAULT_FROM_EMAIL}")
    print(f"  ADMIN_NOTIFY:   {settings.ADMIN_EMAIL_NOTIFICATION or '[NOT SET]'}")
    print("=" * 60)
except Exception as e:
    print(f"[STARTUP] Could not read email config: {e}")
