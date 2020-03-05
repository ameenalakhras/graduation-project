"""
Django settings for composeexample project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url
# from django.contrib.auth.models import User
# heroku or local
database_status = "global"
# heroku or local
server_status = "global"
WEBSITE_NAME = "aug-classroom"
WEBSITE_GLOBAL_URL = f'{WEBSITE_NAME}.herokuapp.com'
USE_S3 = True
USE_AWS_FOR_OFFLINE_USAGE=False
DEBUG = True
# the name for the directory that the settings.py file is in
PROJECT_MAIN_APP_NAME="composeexample"
# database_status = None


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import dj_database_url

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY")


ALLOWED_HOSTS = []

AUTH_USER_MODEL = "authentication.User"
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',
    'rest_framework',

    'authentication',
    'main',
    'classroom',
    'course',
    'mail',
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

ROOT_URLCONF = f'{PROJECT_MAIN_APP_NAME}.urls'

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

WSGI_APPLICATION = f'{PROJECT_MAIN_APP_NAME}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


if server_status == "local":
    ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0"]
    if database_status == "local":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv("POSTGRES_DB"),
                'USER': os.getenv("POSTGRES_USER"),
                'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
                'HOST': os.getenv("POSTGRES_HOST"),
                'PORT': os.getenv("POSTGRES_PORT"),
            }
        }
    elif database_status == "global":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv("GLOBAL_POSTGRES_DB"),
                'USER': os.getenv("GLOBAL_POSTGRES_USER"),
                'PASSWORD': os.getenv("GLOBAL_POSTGRES_PASSWORD"),
                'HOST': os.getenv("GLOBAL_POSTGRES_HOST"),
                'PORT': os.getenv("GLOBAL_POSTGRES_PORT"),
            }
        }

    else:
        raise ValueError("database_status is not recognized.(try to use global or  local ")


elif server_status == "global":
    ALLOWED_HOSTS = [WEBSITE_GLOBAL_URL]
    if database_status == "global":
        DATABASES={}
        DATABASES['default'] = dj_database_url.config()
    else:
        raise("The website can't run a dev(local) database on a global server")

else:
    raise ValueError("server_status is not recognized.(try to use global or  local ")

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/'


# DEFAULT_PATH = "default"
# DEFAULT_USER_PATH = os.path.join(DEFAULT_PATH, 'user')
#
# DEFAULT_USER_AVATAR_PATH = os.path.join(DEFAULT_USER_PATH, 'avatar/index.png')
# DEFAULT_USER_BACKGROUND_PATH = os.path.join(DEFAULT_USER_PATH, 'cover/index.jpg')
#
# DEFAULT_PROJECT_PATH = os.path.join(DEFAULT_PATH, 'project')
# DEFAULT_PROJECT_AVATAR_PATH = os.path.join(DEFAULT_PROJECT_PATH, "avatar/index.png")

# aws s3 settings
if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:

    if USE_AWS_FOR_OFFLINE_USAGE:

        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
        # s3 static settings
        STATIC_LOCATION = 'static'
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
        STATICFILES_STORAGE = f'{PROJECT_MAIN_APP_NAME}.storage_backends.StaticStorage'
        # s3 public media settings
        PUBLIC_MEDIA_LOCATION = 'media'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
        DEFAULT_FILE_STORAGE = f'{PROJECT_MAIN_APP_NAME}.storage_backends.PublicMediaStorage'
        # s3 private media settings
        PRIVATE_MEDIA_LOCATION = 'private'
        PRIVATE_FILE_STORAGE = f'{PROJECT_MAIN_APP_NAME}.storage_backends.PrivateMediaStorage'
    else:
        STATIC_URL = '/static/'
        STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
        MEDIA_URL = '/mediafiles/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
