"""
WSGI config for i2amparis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys
# import environ
#
# env = environ.Env()
# if "SETTINGS" not in env:
#     settings_file = "i2amparis.settings.development"
# else:
#     environ.Env.read_env()
#     settings_file = env("SETTINGS")
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_file)
# sys.path.append('/opt/visualisation_engine')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'i2amparis.settings')

application = get_wsgi_application()
