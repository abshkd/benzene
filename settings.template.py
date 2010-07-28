# Django settings for benzene project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@domain.com'),
)

INTERNAL_IPS = ('127.0.0.1',)

SITE_NAME = 'Benzene Reference' #the name of your site. it can includes spaces. not the URL

SITE_ADDRESS = '192.168.1.100:8000' #the URL of your site, without any protocol at the beginning

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'benzene',					  # Or path to database file if using sqlite3.
		'USER': 'benzene_user',					  # Not used with sqlite3.
		'PASSWORD': '',				  # Not used with sqlite3.
		'HOST': '',					  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',					  # Set to empty string for default. Not used with sqlite3.
	}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.getcwd() + '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://' + SITE_ADDRESS + '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j4(!0&*=f^7o9(qb*$p@t7$%nqy7fls19)bu+@007jmtj9*%cf'

SITE_ID = 1

# List of callables that know how to import templates from various sources.
#add cached when appropriate
TEMPLATE_LOADERS = (
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'benzene.urls'

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'benzene.userbase',
	'haystack',
	'queued_search',
	'benzene.private_messages',
	'debug_toolbar',
)

AUTHENTICATION_BACKENDS = (
	'benzene.userbase.auth_backends.CustomUserModelBackend',
)

CUSTOM_USER_MODEL = 'userbase.CustomUser'

if DEBUG:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
	CACHE_BACKEND = 'locmem://'
	HAYSTACK_SEARCH_ENGINE = 'dummy'
	QUEUE_BACKEND = 'dummy'
	MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
else:
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
	QUEUE_BACKEND = 'memcached'
	QUEUE_MEMCACHE_CONNECTION= 'localhost:11211'
	HAYSTACK_SEARCH_ENGINE = 'solr'
	HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'
	
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/user/'

HAYSTACK_SITECONF = 'benzene.search_sites'
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False