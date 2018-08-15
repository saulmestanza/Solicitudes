"""
Django settings for SeguimientoUCSG project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import raven
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=vkplz21=sjyc&t!34@*r*@actn&!f@2l@%9^+zahon#ua!#t!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '178.128.1.122',
    'localhost',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ######
    'captcha',
    'axes',
    'django_extensions',
    'rest_framework',
    'raven.contrib.django.raven_compat',
    ######
    'administrador',
    'profesor',
    'alumno',
    'reporteria',
    'webservices',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SeguimientoUCSG.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/SeguimientoUCSG/templates',
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # set this explicitly
            ],
        },
    },
]

WSGI_APPLICATION = 'SeguimientoUCSG.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'seguimiento_db',
        'USER': 'seguimiento_user',
        'PASSWORD': '2Tug69@j^v+RY69?8FhmfpddX?VwnVGb',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Django Axes
# https://pypi.python.org/pypi/django-axes

AXES_LOGIN_FAILURE_LIMIT = 3

AXES_USE_USER_AGENT = True

AXES_COOLOFF_TIME = 1

AXES_LOCKOUT_URL = '/administrador/locked/'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_URL = '/static/'
STATIC_URL = 'http://178.128.1.122:8000/static/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '#'

# Email Settings

DEFAULT_SENDERS_EMAIL = ['seguimiento.ucsg@gmail.com',]

DEFAULT_FROM_EMAIL = 'seguimiento.ucsg@gmail.com'

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'seguimiento.ucsg@gmail.com'

EMAIL_HOST_PASSWORD = '7UghzqGUd!mPfnEvFXpvVJSt$d5e!YUS'

EMAIL_PORT = 587

# Sentry Settings

RAVEN_CONFIG = {
    'dsn': 'https://3c681a89e61f48e099f2446f90c8dc74:dbcbd9b5aa21413e9fd2a3efb5b066af@sentry.io/1261575',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(BASE_DIR)),
}

