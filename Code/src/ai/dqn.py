from torch import nn
from src.ai.device import DEVICE


class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.linear1 = nn.Linear(input_size, 50)
        self.activation1 = nn.ReLU()
        self.linear2 = nn.Linear(50, 25)
        self.activation2 = nn.ReLU()
        self.linear3 = nn.Linear(25, output_size)
        self.softmax = nn.Softmax(1)

    def forward(self, x):
        x = x.to(DEVICE)
        x = self.linear1(x)
        x = self.activation1(x)
        x = self.linear2(x)
        x = self.activation2(x)
        x = self.linear3(x)
        x = self.softmax(x)
        x = x.to(DEVICE)
        return x
