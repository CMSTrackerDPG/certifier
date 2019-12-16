"""
ASGI config for dqmhelper project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from .wsgi import *
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dqmhelper.settings")

application = get_default_application()
