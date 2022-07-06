import os
import tensorflow as tf
import re
from tqdm import tqdm
from fuzzywuzzy import fuzz
import json

class Model:
    def __init__(self, name, layers):
        self.name = name
        self.layers = layers


class Layer:
    def __init__(self, name, index, shape, dtype):
        self.detail = name + "," + index + "," + shape + "," + dtype


def load_db():
    db = []

    for model_name in os.listdir("/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios/"):

        try:
            # Load TFLite model and allocate tensors.
            interpreter = tf.lite.Interpreter("/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios/" + model_name)
            interpreter.allocate_tensors()
        except:
            print(model_name, "loading error")
            continue

        details = interpreter.get_tensor_details()
        layers = []
        model = Model(model_name, layers)

        for detail in details:
            #shape = re.sub(' +', ',', str(detail['shape']))[:1] + re.sub(' +', ',', str(detail['shape']))[2:]
            shape = str(detail['shape'])
            layer = Layer(detail['name'], str(detail['index']), shape,
                          re.sub(' +', ',', str(detail['dtype'])))

            layers.append(layer.detail)

        model.layers = layers
        db.append(model)

    return db


def load_target_models():
    targets = []

    for model_name in os.listdir("/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android/"):
        # Load TFLite model and allocate tensors.
        try:
            interpreter = tf.lite.Interpreter("/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android/" + model_name)
            interpreter.allocate_tensors()
        except:
            print(model_name, "loading error")
            continue

        details = interpreter.get_tensor_details()
        layers = []
        model = Model(model_name, layers)


        for detail in details:
            #shape = re.sub(' +', ',', str(detail['shape']))[:1] + re.sub(' +', ',', str(detail['shape']))[2:]
            shape = str(detail['shape'])
            layer = Layer(detail['name'], str(detail['index']), shape,
                          re.sub(' +', ',', str(detail['dtype'])))

            layers.append(layer.detail)

        model.layers = layers
        targets.append(model)

    return targets


def extract_DL_features(path):
    # Load TFLite model and allocate tensors.
    try:
        interpreter = tf.lite.Interpreter(path)
        interpreter.allocate_tensors()
    except:
        print(path, "loading error")
        return None

    details = interpreter.get_tensor_details()
    layers = []
    model = Model(path, layers)

    for detail in details:
        shape = str(detail['shape'])
        layer = Layer(detail['name'], str(detail['index']), shape,
                      re.sub(' +', ',', str(detail['dtype'])))

        layers.append(layer.detail)

    model.layers = layers
    return model


def batch_extract_DL_features(path, save_path):
    models = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if str(file).endswith('.tflite'):
                model_path = os.path.join(root, file)
                model = extract_DL_features(model_path)
                if model is not None:
                    models.append(model)

    with open(save_path, 'w+', encoding='utf8') as f:
        model_features = {}
        for model in models:
            model_features[model.name] = model.layers
        f.write(json.dumps(model_features))

    return models


def main():
    tf_hub_db = load_db()
    targets = load_target_models()

    # compute the structural similarity
    for target in targets:
        results = {}

        for model in tqdm(tf_hub_db):
            results[model.name] = fuzz.ratio(",".join(target.layers), ",".join(model.layers))

        result = {k: v for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True)}

        if result[list(result.keys())[0]] > 0:
            if result[list(result.keys())[0]] > 60:
                print(target.name)
                print(list(result.keys())[0], ":", result[list(result.keys())[0]], "%")
                print(list(result.keys())[1], ":", result[list(result.keys())[1]], "%")
                print(list(result.keys())[2], ":", result[list(result.keys())[2]], "%")
                print(list(result.keys())[3], ":", result[list(result.keys())[3]], "%")
                print()


def model_comparator_json(json1, json2):
    models1_features = json.load(open(json1, 'r', encoding='utf8'))
    models2_features = json.load(open(json2, 'r', encoding='utf8'))
    for k1, v1 in models1_features.items():
        for k2, v2 in models2_features.items():
            similarity = fuzz.ratio(",".join(v1), ",".join(v2))
            print(str(similarity) + ' ' + k1 + ' ' + k2)
            if similarity > 50:
                print(str(similarity) + ' ' + k1 + ' ' + k2)


if __name__ == "__main__":
    #main()

    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android'
    save_path = r'../data/modelComparator/android_model_features.json'
    batch_extract_DL_features(path, save_path)
    json1 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android_model_features.json'
    json2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios_model_features.json'
    # model_comparator_json(json1, json2)