from channels.generic.websocket import AsyncWebsocketConsumer
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from .preprocessing import train_and_evaluate_classifier


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(f"\033[93mDisconnected with code: {close_code}\033[0m")
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json.get('command')
        parameters = text_data_json.get('parameters')
        classifier = text_data_json.get('classifier')

        print(f"\033[92m Received classifier: {classifier}\033[0m")

        if command == 'Train and Test':
            await train_and_evaluate_classifier(self, classifiers_map[classifier], parameters)


classifiers_map = {
    'RandomForest': RandomForestClassifier,
    'DecisionTrees': DecisionTreeClassifier,
    'LogisticRegression': LogisticRegression,
    'SupportVectorMachine': SVC
}
