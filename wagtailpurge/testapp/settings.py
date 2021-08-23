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
    "wagtailpurge.testapp",
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

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "wagtailpurge.testapp.urls"
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
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")
STATIC_URL = "/static/"

# By default, Django uses a computationally difficult algorithm for passwords hashing.
# We don't need such a strong algorithm in tests, so use MD5
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

WAGTAILFRONTENDCACHE = {
    "dummy": {
        "BACKEND": "wagtailpurge.utils.DummyFECacheBackend",
        "LOCATION": "http://localhost:8000",
    },
}

WAGTAILIMAGES_IMAGE_MODEL = "testapp.CustomImage"
