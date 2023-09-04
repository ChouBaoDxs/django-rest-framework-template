"""
Django settings for drf_template project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

ENV = os.getenv('ENV', 'DEVELOP')
DEVELOP = ENV == 'DEVELOP'
PRODUCT = ENV == 'PRODUCT'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!_wun#87=n3zk2h1t#3wc9-9=$63q5fqq-d^6@pr9s%d79yk5i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'crispy_forms',
    'django_extensions',
    'django_filters',
    'django_socio_grpc',
    'drf_yasg',
    'rest_framework',
    'xadmin',

    'user',
    'django_socio_grpc_quickstart',
    'test_demo',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'utils.middlewares.CodeMessageDataMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'utils.middlewares.GetParamsCamelCaseMiddleware',
]

ROOT_URLCONF = 'drf_template.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'drf_template.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DEFAULT_MYSQL_DB_NAME', 'default_db'),
        'USER': os.getenv('DEFAULT_MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('DEFAULT_MYSQL_PASSWORD', '123456'),
        'HOST': os.getenv('DEFAULT_MYSQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('DEFAULT_MYSQL_PORT', '3306'),
        'OPTIONS': {
            'init_command': 'SET sql_mode=STRICT_TRANS_TABLES, innodb_strict_mode=1',
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600  # 连接保持 600 秒，算是优化
    },
    # 'db2': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

APPEND_SLASH = True

# log
LOG_FILE_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_FILE_DIR):
    os.mkdir(LOG_FILE_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(module)s.%(funcName)s] [%(levelname)s - %(message)s]'
        },
    },
    'filters': {

    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'default.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 1,
            'formatter': 'standard',
            'encoding': 'utf8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'error.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 1,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'request': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'request.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 1,
            'formatter': 'standard'
        },
    },
    'loggers': {
        'default': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'request': {
            'handlers': ['request', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'error': {
            'handlers': ['error', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
