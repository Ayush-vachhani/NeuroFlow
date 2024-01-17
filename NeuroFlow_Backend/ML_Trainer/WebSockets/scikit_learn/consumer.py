from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .Classifiers.RandomForests import train_random_forest
from .Classifiers.DecisionTrees import train_decision_trees
from .Classifiers.LogisticRegression import train_logistic_regression
from .Classifiers.SVM import train_svg

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

        print(f"\033[92mReceived classifier: {classifier}\033[0m")

        if command == 'Train and Test':
            if classifier == 'RandomForest':
                await train_random_forest(self, parameters)
            elif classifier == 'DecisionTrees':
                await train_decision_trees(self, parameters)
            elif classifier == 'LogisticRegression':
                await train_logistic_regression(self, parameters)
            elif classifier == 'SVM':
                await train_svg(self, parameters)
