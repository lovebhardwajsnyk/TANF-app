import os
import json
import random
import string
from os.path import join
from distutils.util import strtobool
import dj_database_url
from configurations import Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import jwcrypto.jwk as jwk


class Common(Configuration):

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',


        # Third party apps
        'rest_framework',            # Utilities for rest apis
        'rest_framework.authtoken',  # Token authentication
        'django_filters',            # For filtering rest endpoints
        'mozilla_django_oidc',       # OAuth

        # Local apps
        'tdpservice.users',

    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'mozilla_django_oidc.middleware.SessionRefresh',
    )

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = 'tdpservice.urls'
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    WSGI_APPLICATION = 'tdpservice.wsgi.application'

    # Email Server
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    #Those who will receive error notifications from django via email
    ADMINS = (
        ('Admin1', 'ADMIN_EMAIL_FIRST'),
        ('Admin2', 'ADMIN_EMAIL_SECOND')
    )

    # Postgres
    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://postgres:@postgres:5432/postgres',
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        )
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))
    STATICFILES_DIRS = []
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
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

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'no'))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
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

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO'
            },
        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 10)),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        )
    }

    # OAuth
    AUTHENTICATION_BACKENDS = (
        'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    )
    
    # SECURITY WARNING: keep the secret key used in production secret!
    def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    
    if 'SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['SECRET_KEY']
    else:
        SECRET_KEY = random_generator(100)
    
    # the PEM file here is generated by the deploy script and stored in the env.
    priv_key = jwk.JWK.from_pem(bytes(os.environ['JWT_KEY'], "utf-8"))
    with open('/tmp/priv_key.jwk', 'w') as f:
        key = json.loads(priv_key.export())
        keyset = {'keys': [key]}
        f.write(json.dumps(keyset))
        
    # conditionally set which URI to go to
    if 'VCAP_APPLICATION' in os.environ:
        appjson = os.environ['VCAP_APPLICATION']
        appinfo = json.loads(appjson)
        authuri = 'https://secure.login.gov/'
        if len(appinfo['application_uris']) > 0:
            appdomain = 'https://' + appinfo['application_uris'][0]
        else:
            # We are not a web task, so we have no appuri
            appdomain = ''
    else:
        # we are running locally
        appdomain= 'http://localhost:8000'
        authuri = 'https://idp.int.identitysandbox.gov/'
        
    appuri = appdomain + '/openid/callback/login/'

    OIDC_RP_SIGN_ALGO = 'RS256'
    OIDC_RP_CLIENT_ID = os.environ['OIDC_RP_CLIENT_ID']
    OIDC_RP_CLIENT_SECRET = os.environ['SECRET_KEY']
    OIDC_RP_IDP_SIGN_KEY = os.environ['JWT_KEY']
    
    OIDC_OP_JWKS_ENDPOINT = authuri
    OIDC_OP_AUTHORIZATION_ENDPOINT = authuri + '/openid_connect/authorize'
    OIDC_OP_TOKEN_ENDPOINT = authuri
    OIDC_OP_USER_ENDPOINT = appdomain + '/users'
    
    LOGIN_REDIRECT_URL = appuri
    LOGOUT_REDIRECT_URL = appdomain

