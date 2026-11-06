"""Offline test settings; no application database or Cloudinary credentials used."""
import os

os.environ['DEV'] = '1'

from .settings import *  # noqa: F403,E402

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
MIDDLEWARE = [item for item in MIDDLEWARE if item != 'whitenoise.middleware.WhiteNoiseMiddleware']
