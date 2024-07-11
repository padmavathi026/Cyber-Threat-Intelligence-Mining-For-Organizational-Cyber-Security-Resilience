"""
WSGI( web server gateway interface) communication between web server and python web application config for cyberthreatprediction project.

It exposes the WSGI callable as a module-level variable named ``application``.


"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cyber Threat Prediction.settings')

application = get_wsgi_application()
