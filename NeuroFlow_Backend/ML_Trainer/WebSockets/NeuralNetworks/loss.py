import torch.nn
from torch import nn


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


loss_functions_map = {
    'BCELoss': nn.BCELoss,
    'CrossEntropyLoss': nn.CrossEntropyLoss,
}
