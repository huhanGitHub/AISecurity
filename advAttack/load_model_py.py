import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.autograd import Variable


class Net(nn.Module):
    # define nn
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 128, 128, 3)
        self.pool1 = nn.MaxPool2d(1, 8, 8, 256)
        self.conv2 = nn.Conv2d(1, 64, 64, 32)

        self.conv3 = nn.Conv2d(1, 64, 64, 32)
        self.conv4 = nn.Conv2d(256, 3, 3, 128)

        self.fc1 = nn.Linear(1, 256)
        # self.softmax = nn.Softmax(1, 2)
        self.bn = nn.BatchNorm2d(1, 64, 64, 32)

    def forward(self, x):
        x1 = x
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.conv2(x)

        x1 = F.relu(self.conv1(x1))
        x1 = F.relu(self.conv2(x1))
        x1 = self.conv2(x1)

        x = torch.add(x, x1)
        x = F.relu(self.bn(x))


        x = F.relu(self.conv2(x))
        x = self.conv2(x)
        x = F.relu(self.bn(x))

        x = self.conv3(x)
        x = F.relu(self.conv2(x))
        x = self.conv2(x)
        x = F.relu(self.bn(x))

        x = F.relu(self.conv2(x))
        x = self.conv2(x)
        x = F.relu(self.bn(x))

        x = self.conv3(x)
        x = F.relu(self.conv2(x))
        x = self.conv2(x)
        x = F.relu(self.bn(x))

        x = F.relu(self.conv2(x))
        x = self.conv2(x)
        x = F.relu(self.bn(x))

        x = self.conv4(x)

        x = self.pool1(x)

        x = self.fc1(x)

        x = self.softmax(x)
        # x = x.view(-1, 16 * 5 * 5)

        return x

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
    file1 = open('./models/gender_nn/' + str(i+1) + '_para.txt', 'r')
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    parameters_list = []
    for line in Lines:
        # count += 1
        # print("Line{}: {}".format(count, line.strip()))
        parameters = line.replace('[', '').replace(']', '').split()
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
