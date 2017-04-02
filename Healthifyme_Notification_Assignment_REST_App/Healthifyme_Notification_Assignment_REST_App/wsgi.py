"""
WSGI config for Healthifyme_Notification_Assignment_REST_App project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Healthifyme_Notification_Assignment_REST_App.settings")

application = get_wsgi_application()
