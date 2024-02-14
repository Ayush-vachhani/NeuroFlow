import numpy as np
import random
import asyncio
import json
import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import pandas as pd
from ML_Trainer.WebSockets.scikit_learn.preprocessing import preprocess_data
from .loss import calculate_binary_accuracy

df = pd.read_csv('Data/Titanic/train.csv')
X, y = preprocess_data(df)


class DynamicNet(nn.Module):

    def __init__(self, num_features, hidden_layers):
        super(DynamicNet, self).__init__()
        self.layers = nn.ModuleList()
        prev_layer_size = num_features

        # Iterate through the hidden_layers array
        for layer_info in hidden_layers:
            layer_size = layer_info['No_of_Circles']  # Extract the number of circles (neurons)
            self.layers.append(nn.Linear(prev_layer_size, layer_size))
            prev_layer_size = layer_size

        # Output layer
        self.layers.append(nn.Linear(prev_layer_size, 1))

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            if i < len(self.layers) - 1:
                x = F.tanh(layer(x))
            else:
                x = torch.sigmoid(layer(x))
        return x


async def train_network(self, nn_structure, epochs, split):
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)

    X_tensor = torch.tensor(X.values).float()
    y_tensor = torch.tensor(y.values).long()
    X_train, X_test, y_train, y_test = train_test_split(
        X_tensor, y_tensor, train_size=split/100, random_state=42
    )

    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    test_dataset = TensorDataset(X_test, y_test)

    num_features = X_train.size(1)
    model = DynamicNet(num_features, nn_structure)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001, weight_decay=0.001)

    for epoch in range(epochs):
        model.train()
        for batch, (inputs, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs).squeeze()  # Remove extra dimension from outputs
            loss = criterion(outputs, labels.float())  # Ensure labels are float
            loss.backward()
            optimizer.step()
            if batch % 10 == 0:
                print(f'\033[91mEpoch {epoch + 1}, Batch {batch}, Loss: {loss.item()}\033[0m')

        model.eval()
        with torch.no_grad():
            train_accuracy = calculate_binary_accuracy(y_train, model(X_train).squeeze())
            test_accuracy = calculate_binary_accuracy(y_test, model(X_test).squeeze())

        print(
            f'\033[38;5;200mEpoch {epoch + 1}, Train Accuracy: {train_accuracy}, Test Accuracy: {test_accuracy}\033[0m')
        await self.send(json.dumps(
            {"Train_Accuracy": train_accuracy.item(), "Test_Accuracy": test_accuracy.item(), "Epoch": epoch + 1,
             "Loss": loss.item()}))
        await asyncio.sleep(0.25)
