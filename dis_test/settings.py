"""
Django settings for dis_test project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import yaml

from pathlib import (
    Path,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = os.getenv('HUMORESQUES_CONF') or BASE_DIR / 'project_conf.yaml'


def read_config(config_path):
    config_file = open(
        config_path,
        mode='rt',
        encoding='utf-8',
    )
    with config_path:
        config = yaml.load(
            config_file,
            Loader=yaml.FullLoader,
        )

        return config


config = read_config(CONFIG_PATH)
security_section = config['security']
databases_section = config['databases']
static_section = config['static']
i18n_section = config['internationalization']
customization_section = config['customization']
telegram_section = config['telegram']

DATE_FORMAT = customization_section['DATE_FORMAT']
DATETIME_FORMAT = customization_section['DATETIME_FORMAT']
POST_PREVIEW_LEN = customization_section['POST_PREVIEW_LEN']
POST_PREVIEW_TRAILING = customization_section['POST_PREVIEW_TRAILING']

TELEGRAM_API_ID = telegram_section['API_ID']
TELEGRAM_API_HASH = telegram_section['API_HASH']
TELEGRAM_PHONE = telegram_section['PHONE']
TELEGRAM_SESSION_DIRECTORY = telegram_section['SESSION_DIRECTORY']
TELEGRAM_SESSION = telegram_section['SESSION']
TELEGRAM_CHANNEL = telegram_section['CHANNEL']

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = security_section['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = security_section['DEBUG']

ALLOWED_HOSTS = security_section['ALLOWED_HOSTS']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party apps
    'rest_framework',
    'rangefilter',

    # local apps
    'humoresques',
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

ROOT_URLCONF = 'dis_test.urls'

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

WSGI_APPLICATION = 'dis_test.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = databases_section


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = i18n_section['LANGUAGE_CODE']

TIME_ZONE = i18n_section['TIME_ZONE']

USE_I18N = i18n_section['USE_I18N']

USE_L10N = i18n_section['USE_L10N']

USE_TZ = i18n_section['USE_TZ']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = static_section['STATIC_URL']
STATIC_ROOT = static_section['STATIC_ROOT']

MEDIA_URL = static_section['MEDIA_URL']
MEDIA_ROOT = Path(static_section['MEDIA_ROOT'])
MEDIA_ROOT.mkdir(
    mode=0o755,
    parents=True,
    exist_ok=True,
)
