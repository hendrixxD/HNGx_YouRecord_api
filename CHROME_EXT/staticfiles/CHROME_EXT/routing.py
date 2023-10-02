from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import VideoConsumer

websocket_urlpatterns = [
    path('ws/video_stream/', VideoConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
