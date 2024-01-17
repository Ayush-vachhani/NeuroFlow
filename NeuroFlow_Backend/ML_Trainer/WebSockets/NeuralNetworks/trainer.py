from channels.generic.websocket import AsyncWebsocketConsumer
import json


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send('You are noob')
    async def disconnect(self, close_code):
        print(f"\033[93mDisconnected with code: {close_code}\033[0m")
        await self.close()
