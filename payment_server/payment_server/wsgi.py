"""
WSGI config for payment_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payment_server.settings")

application = get_wsgi_application()
application = WhiteNoise(
    application,
    root=os.path.join(os.path.dirname(os.path.dirname(__file__)), "staticfiles"),
)
