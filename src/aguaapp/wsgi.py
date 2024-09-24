"""
WSGI config for agua project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
print('wsgi 1')
from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise
print('wsgi 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguaapp.settings_local')
os.environ.setdefault('SECRET_KEY','abababababababababab')
print('wsgi 3')
application = get_wsgi_application()
# application = DjangoWhiteNoise(application)
print('wsgi 4')
