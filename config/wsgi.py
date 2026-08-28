"""
WSGI config for Mayank Classes platform.
Compatible with PythonAnywhere, Gunicorn, uWSGI, and Heroku.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
