from django.urls import re_path
from . import consumers
from channels.routing import ProtocolTypeRouter, URLRouter


websocket_urlpatterns = [
    re_path(r"ws/socket-server/", consumers.ChatConsumer.as_asgi())
]


application = ProtocolTypeRouter({"websocket": URLRouter(websocket_urlpatterns)})
