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


class tfliteLayer:
    def __init__(self, name, index, shape, d_type):
        self.detail = name + "," + index + "," + shape + "," + d_type

class coreMLLayer:
    def __init__(self, name, index, shape):
        self.detail = name + "," + index + "," + shape



def load_db():
    db = []

    for model_name in os.listdir("/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios/"):

        try:
            # Load TFLite model and allocate tensors.
            interpreter = tf.lite.Interpreter(
                "/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios/" + model_name)
            interpreter.allocate_tensors()
        except:
            print(model_name, "loading error")
            continue

        details = interpreter.get_tensor_details()
        layers = []
        model = Model(model_name, layers)

        for detail in details:
            # shape = re.sub(' +', ',', str(detail['shape']))[:1] + re.sub(' +', ',', str(detail['shape']))[2:]
            shape = str(detail['shape'])
            layer = tfliteLayer(detail['name'], str(detail['index']), shape,
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
            interpreter = tf.lite.Interpreter(
                "/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android/" + model_name)
            interpreter.allocate_tensors()
        except:
            print(model_name, "loading error")
            continue

        details = interpreter.get_tensor_details()
        layers = []
        model = Model(model_name, layers)

        for detail in details:
            # shape = re.sub(' +', ',', str(detail['shape']))[:1] + re.sub(' +', ',', str(detail['shape']))[2:]
            shape = str(detail['shape'])
            layer = tfliteLayer(detail['name'], str(detail['index']), shape,
                          re.sub(' +', ',', str(detail['dtype'])))

            layers.append(layer.detail)

        model.layers = layers
        targets.append(model)

    return targets


def extract_tflite_features(path):
    # Load TFLite model and allocate tensors.
    try:
        interpreter = tf.lite.Interpreter(path)
        interpreter.allocate_tensors()
    except:
        print(path, "loading error")
        return None

    details = interpreter.get_tensor_details()
    layers = []
    model_name = path[path.rindex('/') + 1:]
    model = Model(path, layers)
    layer_names = []
    for detail in details:
        shape = [str(i) for i in detail['shape']]
        shape = ' '.join(shape)
        name = str(detail['name'])
        # if name == '':
        #     continue
        # if '/' in name:
        #     name = name[:name.index('/')]
        # if name not in layer_names:
        #     layer_names.append(name)

        layer = tfliteLayer(name, str(detail['index']), shape, re.sub(' +', ',', str(detail['dtype'])))
        layers.append(layer.detail)

    model.layers = layers
    return model


def extract_coreml_features(path):
    # Load coreml model
    net = False
    shape = False
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'model.espresso.net' in file:
                net = os.path.join(root, file)
            elif 'model.espresso.shape' in file:
                shape = os.path.join(root, file)

    if net is False or shape is False:
        return None
    else:
        try:
            net_json = json.load(open(net, 'r', encoding='unicode_escape'))
            shape_json = json.load(open(shape, 'r', encoding='unicode_escape'))
            layers = net_json['layers']
            layer_shapes = shape_json['layer_shapes']
            layers_obj = []
            for index, layer in enumerate(layers):
                layer_name = layer['name']
                layer_shape = layer_shapes.get(layer_name, -1)
                if layer_shape == -1:
                    layer_shape = '-1 -1 -1 -1'
                else:
                    layer_shape = str(layer_shape['k']) + ' ' + str(layer_shape['w']) + ' ' + str(layer_shape['n']) + ' ' + str(layer_shape['h'])
                layer_obj = coreMLLayer(layer_name, str(index), layer_shape)
                layers_obj.append(layer_obj.detail)

            if len(layers_obj) == 0:
                return None
            model = Model(path, layers_obj)
            return model
        except json.decoder.JSONDecodeError as e:
            print(str(e) + ' ' + path)
            return None
        except UnicodeDecodeError as e2:
            print(str(e2) + ' ' + path)
            return None


def batch_extract_coreml_features(path, save_path):
    models = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if str(dir).endswith('.mlmodelc'):
                if 'pose_detection' in dir:
                    continue

                model_path = os.path.join(root, dir)
                model = extract_coreml_features(model_path)
                if model is not None:
                    models.append(model)

    with open(save_path, 'w', encoding='utf8') as f:
        model_features = {}
        for model in models:
            model_features[model.name] = model.layers
        f.write(json.dumps(model_features))

    return models


def batch_extract_tflite_features(path, save_path):
    models = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if str(file).endswith('.tflite'):
                if 'pose_detection' in file:
                    continue

                model_path = os.path.join(root, file)
                model = extract_tflite_features(model_path)
                if model is not None:
                    models.append(model)

    with open(save_path, 'w', encoding='utf8') as f:
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
            if k1 == k2:
                continue
            similarity = fuzz.ratio(",".join(v1), ",".join(v2))
            # print(str(similarity) + ' ' + k1 + ' ' + k2)
            if similarity > 50:
                k1_name = k1[str(k1).rindex('/') + 1:]
                k2_name = k2[str(k2).rindex('/') + 1:]
                print(str(similarity) + ' ' + k1 + ' ' + k2)
                if k1_name != k2_name:
                    print(k1_name + '   ' + k2_name)


def model_feature_extraction():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android'
    save_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android_features.json'
    batch_extract_tflite_features(path, save_path)

    path2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios'
    save_path2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios_features.json'
    batch_extract_tflite_features(path2, save_path2)


def modelCompare():
    json1 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android_features.json'
    json2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/ios_features.json'
    model_comparator_json(json1, json2)


if __name__ == "__main__":
    # main()
    # model_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/modelComparator/android/gender_nn.tflite'
    # extract_tflite_features(model_path)
    model_feature_extraction()
    modelCompare()