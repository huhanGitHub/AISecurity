"""
Written by Yujin Huang(Jinx)
Started 22/03/2021 12:35 pm
Last Editted 

Description of the purpose of the code
"""
import tensorflow as tf
import foolbox as fb
import torch
import torch.nn as nn
import torch.nn.functional as F
import foolbox as fb
import numpy as np
from PIL import Image
import os
import eagerpy as ep
import cv2
import matplotlib.pyplot as plt


class Net(nn.Module):
    # define nn
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 512)
        self.fc2 = nn.Linear(512, 10)
        self.dropout1 = nn.Dropout(0.2)

    def forward(self, X):
        # print(X.shape)
        # X = np.array(X)
        X = X.reshape(-1, 784)
        # X = torch.from_numpy(X)
        # X = tf.convert_to_tensor(X, dtype=tf.float32)
        # print(X.shape)
        X = F.relu(self.fc1(X))
        X = self.dropout1(X)
        X = self.fc2(X)

        return X


def save_advs(model_name, attack_name, advs_list):
    # Rescale to 0-255 and convert to uint8, then save adversarial images
    for i, advs in enumerate(advs_list):
        for index, adv in enumerate(advs):
            adv_format = (255.0 / adv.numpy().max() * (adv.numpy() - adv.numpy().min())).astype(
                np.uint8)
            adv_format = np.reshape(adv_format, (28, 28))
            adv_image = Image.fromarray(adv_format)

            path = 'adv_examples/' + model_name + '/' + attack_name + '/' + str(i)
            if not os.path.exists(path):
                os.makedirs(path)
            adv_image.save(path + '/adv' + str(index + 100) + '.png')


def attack():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/advAttack/models/model.pt'
    model = torch.load(path)
    model.eval()
    # model = tf.keras.models.load_model('my_model')

    preprocessing = dict()
    bounds = (0, 1)
    fmodel = fb.PyTorchModel(model, bounds=bounds, preprocessing=preprocessing)
    # fmodel = fb.TensorFlowModel(model, bounds=bounds, preprocessing=preprocessing)

    fmodel = fmodel.transform_bounds((0, 1))
    assert fmodel.bounds == (0, 1)
    images, labels = fb.utils.samples(fmodel, index=0, dataset='mnist', batchsize=27)
    # normalized_input = tf.reshape(images, [20, 784])
    normalized_input = torch.reshape(images, [-1, 3, 3, 3])
    # print(images.shape)
    # print(normalized_input.shape)
    # print(labels.shape)

    print("Accuracy(before attack):", fb.utils.accuracy(fmodel, normalized_input, labels))

    fgsm = fb.attacks.L2ClippingAwareAdditiveGaussianNoiseAttack()

    fgsm_epsilons = np.linspace(1, 1, num=1)

    images = ep.astensor(normalized_input)
    labels = ep.astensor(labels)

    raw, fgsm_advs_list, success = fgsm(fmodel, images, labels, epsilons=fgsm_epsilons)
    save_advs("my_model", 'FGSM', fgsm_advs_list)
    print('FGSM', success.float32().mean().item())


if __name__ == '__main__':
    attack()