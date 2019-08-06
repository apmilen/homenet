"""
Settings Usage:
    1. Environment variables
    2. env/dev.env  (or prod.env, beta.env, ci.env depending on SERVER_ENV)
    3. settings.py defaults (this file)

Settings in this file should be the safest defaults for a PROD environment.
Overrides for dev environments or individual machines should go in env files.
"""

import os
import sys
from decimal import Decimal

from config.system import (
    PLACEHOLDER_FOR_SECRET,
    AttributeDict,
    get_current_django_command,
    get_current_user,
    get_current_hostname,
    get_current_pid,
    get_current_system_time,
    get_python_implementation,
    get_active_git_branch,
    get_active_git_commit,
    load_env_settings,
    check_system_invariants,
    check_prod_safety,
    check_http_settings,
    check_secure_settings,
    check_data_folders,
    get_django_status_line,
    log_django_startup,
)

################################################################################
### Environment Setup
################################################################################
SERVER_ENV = os.getenv('SERVER_ENV', 'UNSET').upper()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.dirname(BASE_DIR)

APP_NAME = 'Homenet'
PROJECT_OWNER = 'Monadical'
PROJECT_NAME = f'{PROJECT_OWNER.lower()}.{APP_NAME.lower()}'
PROJECTS_DIR = '/opt'

HOSTNAME = get_current_hostname()
DJANGO_USER = get_current_user()
PID = get_current_pid()
START_TIME = get_current_system_time()
DJANGO_COMMAND = get_current_django_command()
IS_TESTING = (DJANGO_COMMAND == "test")
IS_MIGRATING = (DJANGO_COMMAND == "migrate")
IS_SHELL = (DJANGO_COMMAND in ('shell', 'shell_plus'))
GIT_HEAD = get_active_git_branch(REPO_DIR)
GIT_SHA = get_active_git_commit(REPO_DIR, GIT_HEAD)
PY_TYPE = get_python_implementation()
IS_TTY = sys.stdout.isatty()

ALLOW_ROOT = False                              # allow django to be run as root (bad)
PROD_SAFETY_CHECK = True                        # enforce that settings are safe for productino environment
MIN_PYTHON_VERSION = (3, 7)                     # minimum python binary version
ALLOWED_ENVS = ('DEV', 'PROD')                  # must match filenamess in env/
ALLOWED_PYTHON_IMPLEMENTATIONS = ('cpython',)   # add 'pypy' here if using PyPy
ALLOWED_REPO_DIR = os.path.abspath(os.path.join(PROJECTS_DIR, PROJECT_NAME))

check_system_invariants(settings=globals())

################################################################################
### Core Django Settings
################################################################################
DEBUG = False
SERVE_STATIC = False
DEFAULT_HOST = 'homenet.zalad.io'
ALLOWED_HOSTS = [DEFAULT_HOST]
DEFAULT_HTTP_PROTOCOL = 'http'
DEFAULT_HTTP_PORT = 443
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MAX_FILE_SIZE = 10485760                        # 10MB
SITE_ID = 1
SECRET_KEY = PLACEHOLDER_FOR_SECRET

SHELL_PLUS = 'ipython'
SHELL_PLUS_PRINT_SQL = False
IPYTHON_ARGUMENTS = ['--no-confirm-exit', '--no-banner']


################################################################################
### Remote Connection Settings
################################################################################

# Don't change values here, only set these values in your env/secrets.env file
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = 5432
POSTGRES_DB = 'penny'
POSTGRES_USER = 'penny'
POSTGRES_PASSWORD = PLACEHOLDER_FOR_SECRET


################################################################################
### Data Location Settings
################################################################################
ENV_DIR = os.path.join(REPO_DIR, 'env')
ENV_DEFAULTS_FILE = os.path.join(ENV_DIR, f'{SERVER_ENV.lower()}.env')
ENV_SECRETS_FILE = os.path.join(ENV_DIR, 'secrets.env')

DATA_DIR = os.path.abspath(os.path.join(REPO_DIR, 'data'))


################################################################################
### Security Settings
################################################################################

X_FRAME_OPTIONS = None                  # handled by nginx
SECURE_BROWSER_XSS_FILTER = False       # handled by nginx
SECURE_CONTENT_TYPE_NOSNIFF = False     # handled by nginx

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

CSRF_COOKIE_SECURE = True               # set False in secrets.env to use http
SESSION_COOKIE_SECURE = True            # set False in secrets.env to use http
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600            # 2 weeks

CORS_ORIGIN_WHITELIST = (               # allow JS from these hosts to query server
    DEFAULT_HOST,
    f'https://{PROJECT_NAME.lower()}.l',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
)
CORS_ORIGIN_ALLOW_ALL = False


################################################################################
### Account Validation Settings
################################################################################
EMAIL_VERIFICATION = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # login via either username or email
ACCOUNT_CONFIRM_EMAIL_ON_GET = True               # easier verification by just clicking a link
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/accounts/email/'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_USERNAME_VALIDATORS = 'ui.views.accounts.username_validators'
PASSWORD_RESET_TIMEOUT_DAYS = 3


################################################################################
### 3rd-Party API Services Config
################################################################################
# Email Provider Settings
MAILGUN_ENABLED = True
MAILGUN_API_KEY = PLACEHOLDER_FOR_SECRET

# Maps Provider Settings
GOOGLE_MAPS_API_KEY = PLACEHOLDER_FOR_SECRET

# Payment Provider Settings
STRIPE_SECRET_KEY = PLACEHOLDER_FOR_SECRET
STRIPE_PUBLISHABLE_KEY = PLACEHOLDER_FOR_SECRET

STRIPE_FEE = Decimal("0.029")  # 2.9% stripe fee
STRIPE_FIXED_FEE = Decimal("0.3")  # 30¢ flat fee

PLAID_PUBLIC_KEY = PLACEHOLDER_FOR_SECRET
PLAID_SECRET_KEY = PLACEHOLDER_FOR_SECRET
PLAID_CLIENT_ID = PLACEHOLDER_FOR_SECRET

################################################################################
### Internationalization & Formatting Settings
################################################################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = True
USE_TZ = True
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d P'
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Load Settings Overrides from Environment Config Files
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# settings defined above in this file (settings.py)
SETTINGS_DEFAULTS = load_env_settings(env=globals())

# settings set via env/SERVER_ENV.env
ENV_DEFAULTS = load_env_settings(dotenv_path=ENV_DEFAULTS_FILE, defaults=globals())
globals().update(ENV_DEFAULTS)

# settings set via env/secrets.env
ENV_SECRETS = load_env_settings(dotenv_path=ENV_SECRETS_FILE, defaults=globals())
globals().update(ENV_SECRETS)

# settings set via environemtn variables
ENV_OVERRIDES = load_env_settings(env=dict(os.environ), defaults=globals())
globals().update(ENV_OVERRIDES)


SETTINGS_SOURCES = {
    'settings.py': SETTINGS_DEFAULTS,
    ENV_DEFAULTS_FILE: ENV_DEFAULTS,
    ENV_SECRETS_FILE: ENV_SECRETS,
    'os.environ': ENV_OVERRIDES,
}
# To track down where a specific setting is being imported from:
# print('Setting sources: \n{SETTINGS_SOURCES}')
# print(config.system.get_setting_source(SETTING_NAME))


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Be careful moving things around below this point, settings depend on the above
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

################################################################################
### Path Settings
################################################################################
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

LOGS_DIR = os.path.join(DATA_DIR, 'logs')
RELOADS_LOGS = os.path.join(LOGS_DIR, 'reloads.log')
DJANGO_SHELL_LOG = os.path.join(LOGS_DIR, 'django_shell.log')

################################################################################
### Django Core Setup
################################################################################

BASE_URL = f'{DEFAULT_HTTP_PROTOCOL}://{DEFAULT_HOST}'
if DEFAULT_HTTP_PORT not in (80, 443):
    BASE_URL = f'{BASE_URL}:{DEFAULT_HTTP_PORT}'

AUTH_USER_MODEL = 'penny.User'
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'anymail',
    'corsheaders',
    'mapbox_location_field',
    'bootstrap4',
    'django_select2',
    'rest_framework',
    'datatables_listview',
    'django_extensions',

    'penny',
    'listings',
    'ui',
    'schedule',
    'leases',
    'job_applications',
    'stripe',
    'payments',
    'weasyprint',
    'listing_collections',
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
    'corsheaders.middleware.CorsMiddleware',

    # To add more middlewares when DEBUG=True see bottom of this file
]

LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

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

# Required permissions for each folder, r=read only, w=read and write
PROJECT_DIRS = {
    REPO_DIR: 'r',
    LOGS_DIR: 'w',
    STATIC_ROOT: 'r',
    MEDIA_ROOT: 'w',
}

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

ACCOUNT_DEFAULT_HTTP_PROTOCOL = DEFAULT_HTTP_PROTOCOL

if MAILGUN_ENABLED:
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    assert MAILGUN_API_KEY != PLACEHOLDER_FOR_SECRET, (
        'MAILGUN_API_KEY must be set in secrets.env if MAILGUN_ENABLED=True'
    )
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ANYMAIL = {
    "MAILGUN_API_KEY": MAILGUN_API_KEY,
    "MAILGUN_SENDER_DOMAIN": DEFAULT_HOST,
}
DEFAULT_FROM_EMAIL = f'support@{DEFAULT_HOST}'
SERVER_EMAIL = f'server@{DEFAULT_HOST}'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'
    ),
    'PAGE_SIZE': 12,
    'DATE_FORMAT': "%b %d, %Y",
    'DATETIME_FORMAT': "%b %d, %Y, %I:%M %p"
}


SELECT2_JS = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.7/js/select2.min.js'
SELECT2_CSS = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.7/css/select2.min.css'

CLI_COLOR = False
if DEBUG:
    CLI_COLOR = IS_TTY
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
    INTERNAL_IPS = ['127.0.0.1']


################################################################################
### Environment Assertions & Init Logging
################################################################################


STATUS_LINE = get_django_status_line(settings=globals(), pretty=False)
PRETTY_STATUS_LINE = get_django_status_line(settings=globals(), pretty=True)

SETTINGS_DICT = AttributeDict(globals())

check_system_invariants(settings=SETTINGS_DICT)
check_prod_safety(settings=SETTINGS_DICT)
check_http_settings(settings=SETTINGS_DICT)
check_secure_settings(settings=SETTINGS_DICT)
check_data_folders(settings=SETTINGS_DICT)


log_django_startup(settings=SETTINGS_DICT)
