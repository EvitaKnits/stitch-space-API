"""
Django settings for stitch_space_api project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import re
if os.path.isfile('env.py'):
    import env
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEV' in os.environ

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [('dj_rest_auth.jwt_auth.JWTCookieAuthentication')],
    'DEFAULT_PAGINATION_CLASS':
        'stitch_space_api.pagination.PageNumberOnlyPagination',
    'PAGE_SIZE': 100, 
}
if 'DEV' not in os.environ:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]
    
# https://medium.com/@michal.drozdze/django-rest-apis-with-jwt-authentication-using-dj-rest-auth-781a536dfb49#:~:text=If%20you%20need%20to%20refresh,%2Ftoken%2Frefresh%2F%20endpoint.
# djangorestframework-simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# dj-rest-auth
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "_auth",  # Name of access token cookie
    "JWT_AUTH_REFRESH_COOKIE": "_refresh", # Name of refresh token cookie
    "JWT_AUTH_HTTPONLY": False,  # Makes sure refresh token is sent
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'stitch_space_api.serializers.CurrentUserSerializer'
}

ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST'),
    '8000-evitaknits-stitchspacea-7teiu88dgwp.ws.codeinstitute-ide.net',
    'evitaknits-stitchspacea-7teiu88dgwp.ws.codeinstitute-ide.net',
    'evitaknits-stitchspace-7onfzh7z8gz.ws.codeinstitute-ide.net',
    'localhost',
    '127.0.0.1',
    ]

CSRF_TRUSTED_ORIGINS = [
    'https://5173-evitaknits-stitchspace-7onfzh7z8gz.ws.codeinstitute-ide.net',
    'https://8000-evitaknits-stitchspacea-7teiu88dgwp.ws.codeinstitute-ide.net']

# CORS_ALLOWED_ORIGINS = [
#     'https://stitch-space-f65c363b25bd.herokuapp.com',
#     'https://5173-evitaknits-stitchspace-7onfzh7z8gz.ws.codeinstitute-ide.net'
# ]

if 'CLIENT_ORIGIN' in os.environ:
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CLIENT_ORIGIN')
    ]
else:
    if 'CLIENT_ORIGIN_DEV' in os.environ:
        extracted_url = re.match(r'^.+-', os.environ.get('CLIENT_ORIGIN_DEV', ''), re.IGNORECASE).group(0)
        CORS_ALLOWED_ORIGIN_REGEXES = [
            rf"*\.codeinstitute-ide\.net$",
        ]

CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',
    'django_filters',
    'profiles',
    'notifications',
    'pieces',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'stitch_space_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'stitch_space_api.wsgi.application'

# Database
# Using sqlite3 for testing to avoid running a separate Postgres DB
if os.environ.get('DEV') == 'TRUE':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default':
            dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }

# Print which database is being used for debugging
# print(DATABASES['default'])


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth for authentication
AUTHENTICATION_BACKENDS = ("allauth.account.auth_backends.AuthenticationBackend",)

# Disable email verification on account creation
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = False