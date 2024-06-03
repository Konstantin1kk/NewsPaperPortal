from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

SITE_ID = 1


INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'news.apps.NewsConfig',
    'accounts',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'NewsPaperProject1.urls'

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
                
                'django.template.context_processors.request'
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'NewsPaperProject1.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / STATIC_URL]
LOGIN_REDIRECT_URL = '/posts'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'NewsPaperPortal'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'NewsPaperPortal@yandex.ru'
EMAIL_SUBJECT_PREFIX = ''

SERVER_EMAIL = 'NewsPaperPortal@yandex.ru'
MANAGERS = (
    ('Petr', 'vostryakov.aleksandr.56@mail.ru'),
)

ADMINS = (
    ('kostya', 'vostryakov.aleksandr.56@mail.ru'),
)

# default:Cl1y3XTrbZJ3CB8je0pLHEqRlsjxeoFh@redis-16105.c1.asia-northeast1-1.gce.cloud.redislabs.com:16105
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files')
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_debug_formatter': {
            'format': '{asctime} {levelname} --[{message}]--',
            'style': '{'
        },
        'console_warning_formatter': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{'
        },
        'error_critical_formatter': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'style': '{'
        },
        'info_formatter': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{'
        },
        'security_formatter': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{'
        },
        'email_formatter': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{'
        }
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },

    'handlers': {
        'debug_console_handler': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'level': 'DEBUG',
            'formatter': 'console_debug_formatter',
        },
        'warning_console_handler': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'level': 'WARNING',
            'formatter': 'console_warning_formatter'
        },
        'info_file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            # сообщения с регистратора django
            'filters': ['require_debug_false'],
            'level': 'INFO',
            'formatter': 'info_formatter'
        },
        'error_console_handler': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'level': 'ERROR',
            'formatter': 'error_critical_formatter'
        },
        'critical_console_handler': {
          'class': 'logging.StreamHandler',
          'filters': ['require_debug_true'],
          'level': 'CRITICAL',
          'formatter': 'error_critical_formatter'
        },
        'error_file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'filters': ['require_debug_false'],
            'level': 'ERROR',
            'formatter': 'error_critical_formatter'
        },
        'critical_file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'filters': ['require_debug_false'],
            'level': 'CRITICAL',
            'formatter': 'error_critical_formatter'
        },
        'security_file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'filters': ['require_debug_false'],
            'level': 'INFO',
            'formatter': 'security_formatter'
        },
        'email_handler': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'email_formatter',
        }
    },

    'loggers': {
        # 'debug_warning_logger': {
        #     'handlers': ['debug_console_handler', 'warning_console_handler'],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
        # 'error_critical_logger': {
        #     'handlers': ['error_console_handler', 'critical_console_handler'],
        #     'level': 'ERROR',
        #     'propagate': False
        # },
        # 'info_logger': {
        #     'handlers': ['info_file_handler'],
        #     'level': 'INFO',
        #     # django.request, django.server, django.template, django.db.backends.
        #     'propagate': False
        # },

        'django.request': {
            'handlers': ['error_file_handler', 'critical_file_handler', 'email_handler'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.server': {
            'handlers': ['error_file_handler', 'critical_file_handler', 'email_handler'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.template': {
            'handlers': ['error_file_handler', 'critical_file_handler'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.security': {
          'handlers': ['security_file_handler'],
          'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['error_file_handler', 'critical_file_handler'],
            'level': 'ERROR',
            'propagate': False
        },
        'django': {
            'handlers': ['debug_console_handler',
                         'warning_console_handler',
                         'error_console_handler',
                         'critical_console_handler',
                         'info_file_handler',],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
