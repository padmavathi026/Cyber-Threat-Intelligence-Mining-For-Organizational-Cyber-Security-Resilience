"""
ASGI config for Cyberthreatprediction project.

It exposes the ASGI callable as a module-level variable named ``application``.


"""
# configure django environment settings 
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cyber Threat Prediction.settings')

application = get_asgi_application()
