import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from NeuroFlow_Backend.WebSockets.scikit_learn import consumer
from NeuroFlow_Backend.WebSockets.NeuralNetworks import trainer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeuroFlow_Backend.settings')

websocket_urlpatterns = [
    path('ws/scikit_learn_socket', consumer.ScikitLearnSocket.as_asgi()),
    path('ws/NeuralNetworks_socket', trainer.TorchTrainer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
