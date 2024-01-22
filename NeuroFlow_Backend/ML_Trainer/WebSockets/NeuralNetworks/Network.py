import asyncio
import json
import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import pandas as pd
from ML_Trainer.WebSockets.scikit_learn.preprocessing import preprocess_data

df = pd.read_csv('Data/Titanic/train.csv')
X, y = preprocess_data(df)

# Convert the DataFrame and Series into PyTorch tensors
X_tensor = torch.tensor(X.values).float()
y_tensor = torch.tensor(y.values).long()

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_tensor, y_tensor, test_size=0.2, random_state=42
)

# Create datasets and dataloaders for training and testing
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

test_dataset = TensorDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)


# Define a simple feedforward neural network
class Net(nn.Module):
    def __init__(self, num_features):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(num_features, 128)
        self.bn1 = nn.BatchNorm1d(128)  # Batch normalization
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)  # Batch normalization
        self.fc3 = nn.Linear(64, 1)  # Output a single value

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = F.dropout(x, p=0.5, training=self.training)
        x = F.relu(self.bn2(self.fc2(x)))
        x = torch.sigmoid(self.fc3(x))  # Apply sigmoid to output
        return x


def calculate_accuracy(y_true, y_pred):
    predicted = torch.argmax(y_pred, 1)
    correct = (predicted == y_true).float()
    accuracy = correct.sum() / len(correct)
    return accuracy.item()


def calculate_binary_accuracy(y_true, y_pred):
    y_pred_tag = torch.round(y_pred)  # Round predictions to 0 or 1
    correct_results_sum = (y_pred_tag == y_true).float().sum()
    accuracy = correct_results_sum / y_true.shape[0]
    return accuracy


async def train_network(self):
    num_features = X_train.size(1)
    model = Net(num_features)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001, weight_decay=0.001)

    for epoch in range(3):
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

        print(f'\033[38;5;200mEpoch {epoch + 1}, Train Accuracy: {train_accuracy}, Test Accuracy: {test_accuracy}\033[0m')
        await self.send(json.dumps({"Train_Accuracy": train_accuracy.item(), "Test_Accuracy": test_accuracy.item(), "Epoch": epoch + 1, "Loss": loss.item()}))
        await asyncio.sleep(0.25)

