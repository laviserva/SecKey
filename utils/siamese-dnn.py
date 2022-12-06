import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
	def __init__(self):
		super(Net, self).__init__() 
		self.conv1 = nn.conv2d(1,6,5)
		self.conv2 = nn.conv2d(6,16,5)
		# an affine operation: y = Wx + b
		self.fc1 = nn.Linear(16 * 5 * 5, 120) #5*5 from image dimension
		self.fc2 = nn.Linear(120, 84)
		self.fc3 = nn.Linear(84,10)

	def forward(self, img_input, db_value: float):
		# Max pooling over a (2,2) window
		img_input = F.max_pool2d(F.relu(self.conv1(img_input)), (2,2) )
		# If the size is square, you can specify with a single number
		img_input = F.max_pool2d(F.relu(self.conv2(img_input), 2)
		img_input = torch.flatten(img_input, 1) # flatten all dimension exceptt the batch dimension

		img_input = F.relu(self.fc1(img_input))
		img_input = F.relu(self.fc2(img_input))
		img_input = self.fc3(img_input)

        error = img_input - db_value
		return error

net = Net()
print(net)

input_1 = torch.randn(1,1,32,32)
out = net(input)