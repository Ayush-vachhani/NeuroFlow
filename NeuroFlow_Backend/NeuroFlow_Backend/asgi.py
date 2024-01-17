import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from ML_Trainer.WebSockets.scikit_learn import consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeuroFlow_Backend.settings')

websocket_urlpatterns = [
    path('ws/scikit_learn_socket', consumer.YourConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
