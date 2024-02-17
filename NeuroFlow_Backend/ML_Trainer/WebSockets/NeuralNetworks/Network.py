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
from .loss import calculate_binary_accuracy, loss_functions_map
from sklearn.metrics import precision_score, recall_score, f1_score

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


async def train_network(self, nn_structure, epochs, split, loss_function):
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
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    num_features = X_train.size(1)
    model = DynamicNet(num_features, nn_structure)
    criterion = loss_functions_map[loss_function]()
    optimizer = optim.Adam(model.parameters(), lr=0.0001, weight_decay=0.001)

    for epoch in range(epochs):
        model.train()
        for batch, (inputs, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs).squeeze()
            loss = criterion(outputs, labels.float())
            loss.backward()
            optimizer.step()
            if batch % 10 == 0:
                print(f'Epoch {epoch + 1}, Batch {batch}, Loss: {loss.item()}')

        # Evaluate model
        model.eval()
        y_pred_list = []
        with torch.no_grad():
            for inputs, _ in test_loader:
                y_test_pred = model(inputs)
                y_test_pred = torch.sigmoid(y_test_pred)
                y_pred_tag = torch.round(y_test_pred)
                y_pred_list.append(y_pred_tag.cpu().numpy())
        y_pred_list = [a.squeeze().tolist() for a in y_pred_list]

        # Flatten the list if predictions are in nested lists
        y_pred_list = [item for sublist in y_pred_list for item in sublist]

        # Calculate precision, recall, and F1 score
        precision = precision_score(y_test.cpu(), y_pred_list, average='binary')
        recall = recall_score(y_test.cpu(), y_pred_list, average='binary')
        f1 = f1_score(y_test.cpu(), y_pred_list, average='binary')

        # Calculate accuracy
        train_accuracy = calculate_binary_accuracy(y_train, model(X_train).squeeze())
        test_accuracy = calculate_binary_accuracy(y_test, model(X_test).squeeze())

        print(f'Epoch {epoch + 1}, Train Accuracy: {train_accuracy}, Test Accuracy: {test_accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}')

        # Send metrics
        await self.send(json.dumps({
            "Train_Accuracy": train_accuracy.item(), "Test_Accuracy": test_accuracy.item(),
            "Epoch": epoch + 1, "Loss": loss.item(), "Precision": precision, "Recall": recall, "F1_Score": f1
        }))
