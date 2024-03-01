from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .Network import train_network


class TorchTrainer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(f"\033[93mDisconnected with code: {close_code}\033[0m")
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        nn_structure = text_data_json.get('hidden_layers')
        epochs = text_data_json.get('epochs')
        split = text_data_json.get('split')
        loss_function = text_data_json.get('loss_function')
        print(text_data)

        await train_network(self, nn_structure, epochs, split, loss_function)
