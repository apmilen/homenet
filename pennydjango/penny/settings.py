"""
Settings Usage:
    1. Environment variables
    2. env/dev.env  (or prod.env, beta.env, ci.env depending on PENNY_ENV)
    3. settings.py defaults (this file)

"""

import os
import sys
import getpass

from time import time


from penny.system import (
    check_system_invariants,
    check_django_invariants,
    chown_django_folders,
    log_django_status_line,
    load_env_settings,
)


PENNY_ENV = os.getenv('PENNY_ENV', 'DEV').upper()
check_system_invariants(PENNY_ENV)


################################################################################
### Environment Setup
################################################################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.dirname(BASE_DIR)

DJANGO_USER = getpass.getuser() or os.getlogin()
HOSTNAME = os.uname()[1]
PID = os.getpid()
START_TIME = time()
IS_TESTING = len(sys.argv) > 1 and sys.argv[1].lower() == "test"
IS_MIGRATING = len(sys.argv) > 1 and sys.argv[1].lower() == "migrate"
IS_SHELL = len(sys.argv) > 1 and sys.argv[1].lower() == 'shell_plus'
GIT_SHA = "someshafornow"
PY_TYPE = sys.implementation.name        # "cpython" or "pypy"
CLI_COLOR = sys.stdout.isatty()
_PLACEHOLDER_FOR_UNSET = 'set-this-value-in-secrets.env'


################################################################################
### Core Django Settings
################################################################################
DEBUG = False
SERVE_STATIC = False
DEFAULT_HOST = 'pennybag.com'
ALLOWED_HOSTS = [DEFAULT_HOST]
INTERNAL_IPS = ['127.0.0.1']
DEFAULT_HTTP_PROTOCOL = 'https'
SECRET_KEY = _PLACEHOLDER_FOR_UNSET
STATIC_URL = '/static/'
SITE_ID = 1

WSGI_APPLICATION = 'penny.wsgi.application'
GRAPHENE = {
    'SCHEMA': 'penny.schema.schema',
    'MIDDLEWARE': []
}
ENDPOINT="http://localhost:8000/graphiql"

SHELL_PLUS = 'ipython'
SHELL_PLUS_PRINT_SQL = False
IPYTHON_ARGUMENTS = ['--no-confirm-exit', '--no-banner']


################################################################################
### Remote Connection Settings
################################################################################

# Don't change values here, set via environment variable or secrets.env file
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = 5432
POSTGRES_DB = 'penny'
POSTGRES_USER = 'penny'
POSTGRES_PASSWORD = ''

################################################################################
### Data Location Settings
################################################################################
ENV_DIR = os.path.join(REPO_DIR, 'env')
ENV_SETTINGS_FILE = os.path.join(ENV_DIR, f'{PENNY_ENV.lower()}.env')
ENV_SECRETS_FILE = os.path.join(ENV_DIR, 'secrets.env')

DATA_DIR = os.path.abspath(os.path.join(REPO_DIR, 'data'))


################################################################################
### Remote Reporting Settings
################################################################################
STDOUT_IO_SUMMARY = DEBUG


################################################################################
### Security Settings
################################################################################
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
X_FRAME_OPTIONS = None
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600  # 2 weeks
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'


################################################################################
### Account Validation Settings
################################################################################
EMAIL_VERIFICATION = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'                # allow login via either username or email
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/accounts/email/'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = DEFAULT_HTTP_PROTOCOL
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_USERNAME_VALIDATORS = 'ui.views.accounts.username_validators'
PASSWORD_RESET_TIMEOUT_DAYS = 3


################################################################################
### 3rd-Party API Services Config
################################################################################
SENTRY_PROJECT_ID = _PLACEHOLDER_FOR_UNSET
SENTRY_DSN_KEY = _PLACEHOLDER_FOR_UNSET
SENTRY_DSN_SECRET = _PLACEHOLDER_FOR_UNSET


ZULIP_SERVER = 'https://monadical.zulip.sweeting.me/api'
ZULIP_EMAIL = 'prod-events-bot@monadical.zulip.sweeting.me'
ZULIP_API_KEY = _PLACEHOLDER_FOR_UNSET

MAILGUN_API_KEY = _PLACEHOLDER_FOR_UNSET


################################################################################
### Internationalization & Formatting Settings
################################################################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = True
USE_TZ = True
SHORT_DATE_FORMAT = 'Y/m/d'
SHORT_DATETIME_FORMAT = 'Y/m/d P'
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','


################################################################################
### Email Settings
################################################################################
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
SUPPORT_GIVERS = [
    # 'max+support@oddslingers.com',
    # 'nick+support@oddslingers.com',
    # 'ana+support@oddslingers.com',
]

INLINE_STATICFILES = False                  # inline JS, and CSS files verbatim instead of inserting a <script> or <link> tag


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Load Settings Overrides from Environment Config Files
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# settings defined above in this file (settings.py)
SETTINGS_DEFAULTS = load_env_settings(env=globals(), defaults=None)

# settings set via env/PENNY_ENV.env
ENV_DEFAULTS = load_env_settings(dotenv_path=ENV_SETTINGS_FILE, defaults=globals())
globals().update(ENV_DEFAULTS)

# settings set via env/secrets.env
ENV_SECRETS = load_env_settings(dotenv_path=ENV_SECRETS_FILE, defaults=globals())
globals().update(ENV_SECRETS)

# settings set via environemtn variables
ENV_OVERRIDES = load_env_settings(env=dict(os.environ), defaults=globals())
globals().update(ENV_OVERRIDES)

SETTINGS_SOURCES = (
    ('settings.py', SETTINGS_DEFAULTS),
    (ENV_SETTINGS_FILE, ENV_DEFAULTS),
    (ENV_SECRETS_FILE, ENV_SECRETS),
    ('os.environ', ENV_OVERRIDES),
)

# print('Setting sources: \n{SETTINGS_SOURCES}')

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Be careful moving things around below this point, settings depend on the above
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Some config should not be in git and can only be passed via secrets or os.env
SECURE_SETTINGS_SOURCES = (ENV_SECRETS_FILE, 'os.environ')
SECURE_SETTINGS = (
    'POSTGRES_PASSWORD',
    'SECRET_KEY',
    'MAILGUN_API_KEY',
    'ZULIP_API_KEY',
    'SENTRY_DSN_KEY',
)

################################################################################
### Path Settings
################################################################################
DEBUG_DUMP_DIR = os.path.join(DATA_DIR, 'debug_dumps')
CACHES_DIR = os.path.join(DATA_DIR, 'caches')

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')

LOGS_DIR = os.path.join(DATA_DIR, 'logs')
RELOADS_LOGS = os.path.join(LOGS_DIR, 'reloads.log')
DJANGO_SHELL_LOG = os.path.join(LOGS_DIR, 'django_shell.log')

DATA_DIRS = [
    LOGS_DIR,
    DEBUG_DUMP_DIR,
    CACHES_DIR,
]

################################################################################
### Django Core Setup
################################################################################
BASE_URL = f'{DEFAULT_HTTP_PROTOCOL}://{DEFAULT_HOST}'

AUTH_USER_MODEL = 'penny.User'
ROOT_URLCONF = 'penny.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'penny',
    'rentals',
    'ui'
]
MIDDLEWARE = [
    'penny.middleware.http2_middleware.HTTP2PushMiddleware',
    'penny.middleware.x_forwarded_for.XForwardedForMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Some more classes are added when DEBUG=True (see bottom of this file)
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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
STATICFILES_DIRS = [STATICFILES_DIR]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'NAME': POSTGRES_DB,
    }
}

ANYMAIL = {
    "MAILGUN_API_KEY": MAILGUN_API_KEY,
    "MAILGUN_SENDER_DOMAIN": DEFAULT_HOST,
}
DEFAULT_FROM_EMAIL = f'support@{DEFAULT_HOST}'
SERVER_EMAIL = f'server@{DEFAULT_HOST}'


if PY_TYPE == 'pypy':
    # Use psycopg2cffi instead of psycopg2 when run with pypy
    from psycopg2cffi import compat
    compat.register()

if IS_TESTING:
    ENABLE_DRAMATIQ = False

if PENNY_ENV == 'CI':
    # Save Junit test timing summary for circleci pretty info display
    TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
    TEST_OUTPUT_DIR = '/tmp/reports/testpy'
    TEST_OUTPUT_FILE_NAME = 'results.xml'

# ANSI Terminal escape sequences for printing colored log messages to terminal
FANCY_STDOUT = CLI_COLOR and DEBUG


if DEBUG:
    # pretty exceptions with context,
    # see https://github.com/Qix-/better-exceptions
    # import better_exceptions  # noqa
    INSTALLED_APPS = [
        'django_pdb',
    ] + INSTALLED_APPS
    MIDDLEWARE = MIDDLEWARE + [
        'django_pdb.middleware.PdbMiddleware'
    ]
    AUTH_PASSWORD_VALIDATORS = []  # don't validate passwords on dev
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    GRAPHENE["MIDDLEWARE"] = ['graphene_django.debug.DjangoDebugMiddleware']

# Assertions about the environment

check_django_invariants()
chown_django_folders()
STATUS_LINE = log_django_status_line()

