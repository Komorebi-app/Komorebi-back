import logging
import os

from datetime import timedelta
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from logs.handler import InterceptHandler

load_dotenv('.env')

ENV_NEEDS = [
    'SECRET_KEY',
    'DJANGO_DEBUG',
    'ALLOWED_HOSTS',
    'CSRF_TRUSTED_ORIGINS',
    'CORS_ALLOWED_ORIGINS',
    'CORS_ALLOWED_ORIGIN_REGEXES',
    'PAGINATION',
    'POSTGRES_DB',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_PORT',
    'POSTGRES_HOST'
]

for x in ENV_NEEDS:
    ENV = os.getenv(x)
    if not ENV:
        raise ValueError(f"{x} environment variable not set")

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DJANGO_DEBUG') == 'True'

ALLOWED_HOSTS = cast(str, os.getenv('ALLOWED_HOSTS')).split(',')
CSRF_TRUSTED_ORIGINS = cast(str, os.getenv('CSRF_TRUSTED_ORIGINS')).split(',')
CORS_ALLOWED_ORIGINS = cast(str, os.getenv('CORS_ALLOWED_ORIGINS')).split(',')

raw_whitelist = os.getenv('CORS_ALLOWED_ORIGIN_REGEXES', '')
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"{}".format(reg.strip()) # pylint: disable=consider-using-f-string
    for reg in raw_whitelist.split(',')
    if reg.strip()
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Application definition

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'drf_redesign',
    'core.apps.CoreConfig',
    'logs.apps.LogsConfig',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
]

UNFOLD = {
    'SITE_TITLE': 'Komorebi',
    'SITE_HEADER': 'Komorebi',
    'SITE_SYMBOL': 'speed',
    'SITE_ICON': {
        'light': '/static/images/logo.webp',
        'dark': '/static/images/logo.webp',
    },
    'COLORS': {
        'primary': {
            '50': '#ecfdf5',
            '100': '#d1fae5',
            '200': '#a7f3d0',
            '300': '#6ee7b7',
            '400': '#34d399',
            '500': '#10b981',
            '600': '#059669',
            '700': '#047857',
            '800': '#065f46',
            '900': '#064e3b',
            '950': '#022c22',
        },
    },
    'SITE_FAVICONS': [
        {
            'rel': 'icon',
            'sizes': '32x32',
            'type': 'image/webp',
            'href': '/static/images/logo.webp',
        },
    ],
    'BORDER_RADIUS': '10px',
    'SIDEBAR': {
        'show_search': True,
        'navigation': [
            {
                'title': 'Library',
                'items': [
                    {
                        'title': 'Authors',
                        'icon': 'group',
                        'link': '/admin/core/author/',
                    },
                    {
                        'title': 'Books',
                        'icon': 'book',
                        'link': '/admin/core/book/',
                    },
                    {
                        'title': 'Collection',
                        'icon': 'format_list_bulleted',
                        'link': '/admin/core/library/',
                    },
                ],
            },
            {
                'title': 'Auth',
                'items': [
                    {
                        'title': 'Users',
                        'icon': 'group',
                        'link': '/admin/auth/user/',
                    },
                ],
            },
        ],
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': int(os.getenv('PAGINATION')),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'HealthIA API',
    'DESCRIPTION': 'API documentation for HealthIA',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAdminUser'
    ],
}

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
    'logs.middleware.logging.LoggingMiddleware',
]

ROOT_URLCONF = 'komorebi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'komorebi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

if os.getenv('DATABASE_URL') == "sqlite:///:memory:":
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

logging.basicConfig(handlers=[InterceptHandler()], level=0)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = False

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
