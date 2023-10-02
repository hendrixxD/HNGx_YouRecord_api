"""
ASGI config for CHROME_EXT project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from . import routing  # Import your routing configuration
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CHROME_EXT.settings')

application = get_asgi_application()

# application = get_asgi_application()
# application = ProtocolTypeRouter({
#    'http': get_asgi_application(),
#    'websocket': routing.application,  # Use the routing configuration for WebSocket connections
# })
