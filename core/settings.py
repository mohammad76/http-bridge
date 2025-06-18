import os
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from . import env

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", env.SECRET_KEY)
DEBUG = os.getenv("DEBUG", env.DEBUG)
NODE_NAME = os.getenv("NODE_NAME", env.NODE_NAME)
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ["http://localhost", f"http://{NODE_NAME}.chabokan.net", f"https://{NODE_NAME}.chabokan.net",
                        f"http://{NODE_NAME}.chabokanco.ir", f"https://{NODE_NAME}.chabokanco.ir"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    # libs
    'rest_framework',
    'rest_framework.authtoken',
    'background_task',
    'django_extensions',
    'import_export',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
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

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

APPEND_SLASH = True

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", env.S3_ACCESS_KEY)
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", env.S3_SECRET_KEY)
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", env.S3_ENDPOINT_URL)

S3_NEW_ACCESS_KEY = os.getenv("S3_NEW_ACCESS_KEY", env.S3_NEW_ACCESS_KEY)
S3_NEW_SECRET_KEY = os.getenv("S3_NEW_SECRET_KEY", env.S3_NEW_SECRET_KEY)
S3_NEW_ENDPOINT_URL = os.getenv("S3_NEW_ENDPOINT_URL", env.S3_NEW_ENDPOINT_URL)

S3_ACCESS_KEY_LAST_BACKUP = os.getenv("S3_ACCESS_KEY_LAST_BACKUP", env.S3_ACCESS_KEY_LAST_BACKUP)
S3_SECRET_KEY_LAST_BACKUP = os.getenv("S3_SECRET_KEY_LAST_BACKUP", env.S3_SECRET_KEY_LAST_BACKUP)
S3_ENDPOINT_URL_LAST_BACKUP = os.getenv("S3_ENDPOINT_URL_LAST_BACKUP", env.S3_ENDPOINT_URL_LAST_BACKUP)

NODE_IP = os.getenv("NODE_IP", env.NODE_IP)
PROXY_IPS = os.getenv("PROXY_IPS", env.PROXY_IPS)

DISABLE_ADMIN = os.getenv("DISABLE_ADMIN", env.DISABLE_ADMIN)

LIMIT_DISK = True

if hasattr(env, 'LIMIT_DISK'):
    LIMIT_DISK = env.LIMIT_DISK

STORAGE_PLATFORMS = ["minio", "ftp", "nextcloud", "registry", "filerun"]

NOTIFICATION_HOOK_URL = "https://hooks.slack.com/services/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"

if DEBUG:
    from .debug_settings import *
else:
    from .production_settings import *
