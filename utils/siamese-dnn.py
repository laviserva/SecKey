import torch
import torch.nn as nn
import torch.nn.functional as F

class SiameseNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.linear1 = nn.Linear(1, 3)
        self.act1 = nn.ReLU()
        self.linear2 = nn.Linear(3, 2)
    
    def forward(self, x_1, x_2):
        x_1 = self.linear1(x_1)
        x_1 = self.act1(x_1)
        x_1 = self.linear2(x_1)
        
        out = x_1 - x_2
        return out

net = SiameseNetwork()
print(net)

input_1 = torch.randn(3,1)
input_2 = torch.randn(3,1)
out = net(input_1, input_2)
print(out)