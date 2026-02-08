from django.contrib import admin
from django.urls import path, include

"""
Root URL configuration.

- /admin/ → Django admin panel
- /api/ → Calculator app APIs
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("calculator.urls")),
]
