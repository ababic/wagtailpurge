import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "NAME": "wagtailpurge-test.sqlite",
        "ENGINE": "django.db.backends.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default-location",
    },
    "secondary": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "tertiary": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

INSTALLED_APPS = (
    "wagtailpurge",
    "wagtailpurge.tests",
    "modelcluster",
    "taggit",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.sites",
    "wagtail.search",
    "wagtail.users",
    "wagtail.images",
    "wagtail.documents",
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.modeladmin",
)

ROOT_URLCONF = "wagtailpurge.tests.urls"
WAGTAIL_SITE_NAME = "Wagtailpurge"
LOGIN_URL = "wagtailadmin_login"
LOGIN_REDIRECT_URL = "wagtailadmin_home"
SECRET_KEY = "fake-key"

# Django i18n
TIME_ZONE = "Europe/London"
USE_TZ = True

# Used in Wagtail emails
BASE_URL = "https://localhost:8000"

# Don't redirect to HTTPS in tests
SECURE_SSL_REDIRECT = False

# Use default static files storage for tests
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# By default, Django uses a computationally difficult algorithm for passwords hashing.
# We don't need such a strong algorithm in tests, so use MD5
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

WAGTAILFRONTENDCACHE = {
    "dummy": {
        "BACKEND": "wagtailpurge.utils.DummyFECacheBackend",
        "LOCATION": "http://localhost:8000",
    },
}
