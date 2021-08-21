DEBUG = False

TIME_ZONE = 'Europe/London'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'

DATABASES = {
    'default': {
        'NAME': 'wagtailpurge-test.sqlite',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'wagtailpurge',
    'wagtailpurge.tests',
    'taggit',
    'modelcluster',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.sites',
    'wagtail.search',
    'wagtail.users',
    'wagtail.images',
    'wagtail.documents',
    'wagtail.contrib.frontendcache',
    'wagtail.contrib.modeladmin',
)

ROOT_URLCONF = 'wagtailpurge.tests.urls'
WAGTAIL_SITE_NAME = 'Wagtailpurge'
LOGIN_URL = 'wagtailadmin_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'
SECRET_KEY = 'fake-key'
