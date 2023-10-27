"""
WSGI config for portal_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()


# Apply WSGI middleware here.
def health_check(application, health_url):
    def health_check_wrapper(environ, start_response):
        if environ.get("PATH_INFO") == health_url:
            start_response("200 OK", [("Content-Type", "text/plain")])
            return []
        return application(environ, start_response)

    return health_check_wrapper


application = health_check(application, "/health")
