from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .Network import train_network


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(f"\033[93mDisconnected with code: {close_code}\033[0m")
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'start_training':
            await train_network(self)

