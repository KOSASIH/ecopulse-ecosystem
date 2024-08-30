import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

class NeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class ConvolutionalNeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(ConvolutionalNeuralNetwork, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.fc1 = nn.Linear(320, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(torch.max_pool2d(self.conv1(x), 2))
        x = torch.relu(torch.max_pool2d(self.conv2(x), 2))
        x = x.view(-1, 320)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class RecurrentNeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(RecurrentNeuralNetwork, self).__init__()
        self.rnn = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.zeros(2, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(2, x.size(0), self.hidden_dim).to(x.device)
        out, _ = self.rnn(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class Model:
    def __init__(self, input_dim, hidden_dim, output_dim, learning_rate, model_type):
        if model_type == 'nn':
            self.model = NeuralNetwork(input_dim, hidden_dim, output_dim)
        elif model_type == 'cnn':
            self.model = ConvolutionalNeuralNetwork(input_dim, hidden_dim, output_dim)
        elif model_type == 'rnn':
            self.model = RecurrentNeuralNetwork(input_dim, hidden_dim, output_dim)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def train(self, X_train, y_train):
        self.model.train()
        self.optimizer.zero_grad()
        outputs = self.model(X_train)
        loss = self.criterion(outputs, y_train)
        loss.backward()
        self.optimizer.step()

    def evaluate(self, X_test, y_test):
        self.model.eval()
        outputs = self.model(X_test)
        _, predicted = torch.max(outputs, 1)
        return predicted

    def predict(self, X_test):
        self.model.eval()
        outputs = self.model(X_test)
        _, predicted = torch.max(outputs, 1)
        return predicted

    def evaluate_metrics(self, y_pred, y_test):
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        matrix = confusion_matrix(y_test, y_pred)
        return accuracy, report, matrix
