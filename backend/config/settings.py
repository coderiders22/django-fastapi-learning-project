from pathlib import Path
import os
import dj_database_url

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# CORE SETTINGS
# =====================

"""
SECRET_KEY:
- Used by Django for cryptographic signing
- In production, this is provided via environment variable
- A fallback value is kept only for local testing
"""
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")

"""
DEBUG:
- Must be False in production
- Enabled locally using environment variable
"""
DEBUG = os.environ.get("DEBUG", "False") == "True"


# =====================
# ALLOWED HOSTS
# =====================

"""
Defines which domains are allowed to serve this Django app.
Required for security reasons.
"""
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".koyeb.app",
    ".onrender.com",
]


# =====================
# APPLICATIONS
# =====================

"""
INSTALLED_APPS:
- Default Django apps
- Django REST Framework for APIs
- corsheaders for frontend-backend communication
- calculator is the main custom app
"""
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "calculator",
]


# =====================
# MIDDLEWARE
# =====================

"""
Middleware order matters.

corsheaders must come first so that CORS headers are added
before any authentication or CSRF checks happen.
"""
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
     "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


# =====================
# URLS & TEMPLATES
# =====================

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# =====================
# DATABASE CONFIGURATION
# =====================

"""
Production database:
- Uses DATABASE_URL provided by Koyeb
- dj_database_url automatically parses Postgres URL
"""
if "DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        )
    }

"""
Local database (PostgreSQL)
Uncomment only when running locally.
"""
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "calculator_db",
#         "USER": "calculator_user",
#         "PASSWORD": "calculator123",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }


# =====================
# PASSWORD VALIDATION
# =====================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =====================
# LANGUAGE & TIMEZONE
# =====================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True


# =====================
# STATIC FILES
# =====================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =====================
# CORS CONFIGURATION
# =====================

"""
Allows frontend (Vercel) to communicate with backend (Koyeb)
while using cookies for authentication.
"""
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://django-fastapi-learning-project.vercel.app",
    "https://calculatorpro-django-backend.koyeb.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
    r"^https://.*\.koyeb\.app$",
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS + [
    "https://django-fastapi-learning-project.vercel.app", 
    "https://calculatorpro-django-backend.koyeb.app"
]


# =====================
# SESSION & CSRF
# =====================

"""
Session-based authentication settings.
Required because the app uses Django sessions
instead of token-based authentication.
"""

SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # frontend needs access to csrftoken

SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN")
CSRF_COOKIE_DOMAIN = os.environ.get("CSRF_COOKIE_DOMAIN")

CSRF_COOKIE_NAME = "csrftoken"
CSRF_USE_SESSIONS = False


# =====================
# SECURITY SETTINGS
# =====================

"""
Koyeb handles HTTPS termination.
Django needs to trust proxy headers.
"""
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

