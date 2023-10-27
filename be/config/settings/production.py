from .base import *

# CORS_ORIGIN
CORS_ORIGIN_WHITELIST = env("CORS_ORIGIN_WHITELIST", default="http://localhost:3000").split(",")
