from .base import *

# GENERAL
DEBUG = True
ALLOWED_HOSTS = ["*"]

from corsheaders.defaults import default_headers


CORS_ALLOW_HEADERS = default_headers + ("responsetype",)
EVENTSTREAM_ALLOW_ORIGIN = "*"