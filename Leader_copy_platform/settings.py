import os
from pathlib import Path

# import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-58^y1r90w=lo=zmwk@e#g-ke!7yquggu%#zl40f33&v55fwapz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Bot'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'Leader_copy_platform.urls'

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

WSGI_APPLICATION = 'Leader_copy_platform.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {'default': dj_database_url.config()}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'CONN_MAX_AGE': 60,
#         "timeout": 35,
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'u168842127_copytrade',
        'USER': 'u168842127_copytrade',
        'PASSWORD': 'Copytrade22',
        'HOST': 'sql980.main-hosting.eu',
        'PORT': '3306',
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menus': [{
        'name': 'Bot',
        'icon': 'fab fa-android',
        'models': [{
            'name': 'ADMINS',
            'url': 'Bot/admin/',
            'icon': 'fas fa-user-ninja'
        }, {
            'name': 'Users',
            'icon': 'fa fa-user',
            'url': 'Bot/users/'
        }, {
            'name': 'Signal',
            'url': 'Bot/signal/',
            'icon': 'fas fa-address-book'
        }, {
            'name': 'TRADERS',
            'url': 'Bot/traders/',
            'icon': 'fas fa-address-book'
        }, {
            'name': 'ClosePosition',
            'url': 'Bot/closeposition/',
            'icon': 'fas fa-address-book'
        }]
    }, {
        'app': 'auth',
        'name': 'Permission',
        'icon': 'fas fa-user-shield',
        'models': [{
            'name': 'Site Users',
            'icon': 'fa fa-user',
            'url': 'auth/user/'
        }, {
            'name': 'Group',
            'icon': 'fas fa-users',
            'url': 'auth/group/'
        }]
    }, ]
}
