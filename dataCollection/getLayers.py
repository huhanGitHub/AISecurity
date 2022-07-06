import os
import json

def getLayers():
    # expressoFile= r'/Users/hhuu0025/Downloads/ipa dataset/pairs/com.voiapp.voi_1395921017_v6.104.1_194/Payload/voi-app.app/best.mlmodelc/model.espresso.net'
    expressoFile = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/model.espresso.net'
    expresso = json.load(open(expressoFile))
    layers = expresso['layers']

    for layer in layers:
        name = layer['type']
        print(name)


def convert2Coreml():
    tf_models = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/model15_fp32_820.tflite'



if __name__ == '__main__':
    getLayers()