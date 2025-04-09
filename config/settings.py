import os
from pathlib import Path
import environ
from datetime import timedelta

# Initialise environment variables
env = environ.Env()

environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-j7@4hld$45*j_&b*0))em!)o1ibj-^se@1=f!=ibt1mq6zo3&r'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'core',
    'articles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_yasg',
    'django_redis',
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

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'core.User'

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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# تنظیمات SendGrid
SENDGRID_API_KEY = 'SENDGRID_API_KEY'
SENDGRID_VERIFICATION_TEMPLATE_ID = ('SENDGRID_VERIFICATION_TEMPLATE_ID')
DEFAULT_FROM_EMAIL = 'noreply@example.com'

# تنظیمات ارسال ایمیل (رایگان)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
DEFAULT_FROM_EMAIL = 'noreply@example.com'

# تنظیمات کاوه‌نگار
KAVENEGAR_API_KEY = 'KAVENEGAR_API_KEY'
KAVENEGAR_SENDER = 'KAVENEGAR_SENDER' # شماره اختصاصی
KAVENEGAR_OTP_TEMPLATE = 'KAVENEGAR_OTP_TEMPLATE'

# تنظیمات REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# تنظیمات JWT
JWT = {
    'SECRET_KEY': 'JWT_SECRET_KEY',
    'ALGORITHM': 'HS512',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# تنظیمات Redis برای کش
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# تنظیمات مربوط به ماژول مقالات
ARTICLE_SETTINGS = {
    'DEFAULT_STATUS': 'draft',
    'MAX_TAGS_PER_ARTICLE': 5,
    'COMMENT_MODERATION': True,
    'AUTO_SLUG': True,
    'DEFAULT_CATEGORY': 'general',
}

# تنظیمات خطاهای مقالات
ARTICLE_ERROR_CONFIG = {
    'MAX_TITLE_LENGTH': 200,
    'MIN_CONTENT_LENGTH': 300,
    'MAX_TAGS': 5,
}

COMMENT_ERROR_CONFIG = {
    'MIN_LENGTH': 10,
    'MAX_LENGTH': 1000,
    'MAX_REPLY_DEPTH': 3,
    'SPAM_KEYWORDS': ['تبلیغ', 'اسپم', 'خرید', 'فروش'],
}

# تنظیمات جستجو
SEARCH_CONFIG = {
    'MIN_SEARCH_LENGTH': 3,
    'MAX_RESULTS': 50,
    'HIGHLIGHT_TAG': '<mark>',
}

# تنظیمات کش
CACHE_TTL = {
    'ARTICLE_DETAIL': 60 * 15,  # 15 دقیقه
    'ARTICLE_LIST': 60 * 5,     # 5 دقیقه
}


ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}
