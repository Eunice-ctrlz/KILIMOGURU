"""
WSGI config for KILIMO GURU project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kilimo_guru.settings')

application = get_wsgi_application()
