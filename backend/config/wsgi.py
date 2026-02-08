"""
WSGI configuration for the project.

WSGI (Web Server Gateway Interface) is used by traditional
Python web servers like Gunicorn or uWSGI.

This file is required for production deployment on platforms
like Koyeb, Render, etc.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# WSGI application callable
application = get_wsgi_application()
