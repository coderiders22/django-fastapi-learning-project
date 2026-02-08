"""
ASGI configuration for the project.

ASGI (Asynchronous Server Gateway Interface) is mainly used for
async features like WebSockets, background tasks, etc.

In this project, ASGI is included for completeness and future scalability,
even though the app currently runs using standard HTTP requests.
"""

import os
from django.core.asgi import get_asgi_application

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# ASGI application callable
application = get_asgi_application()
