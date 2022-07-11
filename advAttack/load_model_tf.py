import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.autograd import Variable


class Net(nn.Module):
    # define nn
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 512)
        self.fc2 = nn.Linear(512, 10)
        self.dropout1 = nn.Dropout(0.2)

    def forward(self, X):
        # print(X.shape)
        X = X.reshape(-1, 784)
        # print(X.shape)
        X = F.relu(self.fc1(X))
        X = self.dropout1(X)
        X = self.fc2(X)

        return X

#Define normalization
transform=transforms.Compose([transforms.ToTensor()])

#Load dataset
# datasets.MNIST.resources = [
#             ('https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz'),
#             ('https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz'),
#             ('https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz'),
#             ('https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz')
#         ]

dataset1 = datasets.MNIST('./data/', train=True, download=True,
                   transform=transform)
dataset2 = datasets.MNIST('./data/', train=False,
                   transform=transform)
train_loader = torch.utils.data.DataLoader(dataset1, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset2, batch_size=64, shuffle=True)

#Build the model we defined above
model = Net()

#Read the parameters file
parameters_dict = {}

for i in range(4):
    file1 = open('./my_model/' + str(i+1) + '_para.txt', 'r')
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    parameters_list = []
    for line in Lines:
        # count += 1
        # print("Line{}: {}".format(count, line.strip()))
        parameters = line.replace('[','').replace(']','').split()
        # print(parameters)
        for record in parameters:
            parameters_list.append(float(record))

    # print(parameters_list)
    parameters_dict[i] = parameters_list

# print(parameters_dict)
model.eval()
test_loss = 0
correct = 0


for data, target in test_loader:
    # print(data.shape)
    data = Variable(data, requires_grad=True)
    target = Variable(target)
    # print(data.shape)
    output = model(data)
    test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
    pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
    correct += pred.eq(target.view_as(pred)).sum().item()

test_loss /= len(test_loader.dataset)

print("First evaluation")
print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
    test_loss, correct, len(test_loader.dataset),
    100. * correct / len(test_loader.dataset)))


# Set the parameters in Net
weight_l0 = parameters_dict[2]
weight_l0_tensor = torch.reshape(torch.Tensor(weight_l0), (512,784))

bias_l0 = parameters_dict[0]
bias_l0_tensor = torch.reshape(torch.Tensor(bias_l0), (1, 512))

weight_l1 = parameters_dict[3]
weight_l1_tensor = torch.reshape(torch.Tensor(weight_l1), (10, 512))

bias_l1 = parameters_dict[1]
bias_l1_tensor = torch.reshape(torch.Tensor(bias_l1), (1, 10))

model.fc1.weight.data = weight_l0_tensor
model.fc1.bias.data = bias_l0_tensor
model.fc2.weight.data = weight_l1_tensor
model.fc2.bias.data = bias_l1_tensor

model.eval()
test_loss = 0
correct = 0
# with torch.no_grad():

for data, target in test_loader:
    data_var = Variable(data, requires_grad = True)
    output = model(data_var)
    loss = F.nll_loss(output, target, reduction='sum')
    test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
    loss.backward()
    print(data_var.grad)
    pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
    correct += pred.eq(target.view_as(pred)).sum().item()


test_loss /= len(test_loader.dataset)

print("Second evaluation")
print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
    test_loss, correct, len(test_loader.dataset),
    100. * correct / len(test_loader.dataset)))


torch.save(model, "simple_model_info/new_my_model.pt")
