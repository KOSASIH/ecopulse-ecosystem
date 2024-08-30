import torch
import torch.nn as nn
import torch.optim as optim

class NeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class Model:
    def __init__(self, input_dim, hidden_dim, output_dim, learning_rate):
        self.model = NeuralNetwork(input_dim, hidden_dim, output_dim)
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
