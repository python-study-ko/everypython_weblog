# -*- coding: utf-8 -*-

"""
WSGI config for everpython project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

# ini파일 호출
from configparser import RawConfigParser
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = RawConfigParser()
config.read(os.path.join(BASE_DIR, 'settings.ini'))
switch_whitnoise = config.get('deploy','WHITENOISE')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "everpython.settings")
if switch_whitnoise == 'True':
    application = DjangoWhiteNoise(get_wsgi_application())
elif switch_whitnoise == 'False':
    application = get_wsgi_application()