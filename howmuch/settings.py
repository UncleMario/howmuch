# Django settings for howmuch project.
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
import os
import dj_database_url

gettext_noop = lambda s: s



DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Juan Carlos Cayetano', 'kayethano@gmail.com'),
)

AUTH_PROFILE_MODULE = 'perfil.perfil'

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://kayethano:90ldenb0y@localhost:5432/howmuch')}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-MX'

LANGUAGES = (

('es-mx', gettext_noop('Mexican Spanish')),

)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

#Site Root
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


#AMAZON
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJBJPT42ROYJRYKFA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'howmuch'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#AMAZON

#FILES

#MEDIA_ROOT = '/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
#STATIC_ROOT = '/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
#S3_URL = 'http://%s.s3-website-us-east-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#STATIC_URL = S3_URL + STATIC_ROOT
STATIC_URL = '/static/'
#MEDIA_URL = S3_URL + MEDIA_ROOT
MEDIA_URL = '/media/'
#DEFAULT_FILE_STORAGE = 'howmuch.s3utils.MediaRootS3BotoStorage'
#STATICFILES_STORAGE = 'howmuch.s3utils.StaticRootS3BotoStorage'

#FILES

#REGISTRATION
ACCOUNT_ACTIVATION_DAYS = 7
#REGISTRATION



# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1afjnj#t5sf=d3n@1v#0)a=y$j-3818co1j5bm988!gqdhzg_w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'howmuch.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'howmuch.wsgi.application'

TEMPLATE_DIRS = ( os.path.join(SITE_ROOT, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'kombu.transport.django',
    'djcelery',
    'howmuch.pictures',
    'smart_selects',
    'howmuch.items',
    'howmuch.core',
    'storages',
    'registration',
    'howmuch.perfil',
    'captcha',
    'howmuch.messages',
    'howmuch.prestige',
    'howmuch.searchengine',
    'howmuch.backend',
    'howmuch.notifications',
    'endless_pagination',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BROKER_BACKEND = 'django'

LOGIN_REDIRECT_URL = '/'

#EMAIL

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'app7604709@heroku.com'
EMAIL_HOST_PASSWORD = 'f1djpkod'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'howmuch@howmuch'

#EMAIL