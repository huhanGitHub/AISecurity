import os
import json

DL_model_fields = ['.tflite', '.model', '.mlmodelc', '.mlmodel', '.pt', '.pb', '.h5', '.tfl', 'cfg']


def inspectAPP(src, DL_models):
    models = []
    for root, dirs, files in os.walk(src):
        for file in files:
            suffix = file[str(file).rfind('.'):]
            if suffix in DL_model_fields:
                print('found DL model')
                models.append(file)

    if len(models) > 0:
        DL_models[src] = models


def batch_inspectAPP(path):
    DL_models = {}
    save_json = r'../data/IOS_models_ase.json'
    org_models = {}
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if str(dir).endswith('.app'):
                app_path = os.path.join(root, dir)
                print(app_path)
                inspectAPP(app_path, DL_models)

    with open(save_json, 'r', encoding='utf8') as f:
        org_models = json.load(f)

    if org_models:
        DL_models = org_models | DL_models
    json_str = json.dumps(DL_models)
    with open(save_json, 'w', encoding='utf8') as f2:
        f2.write(json_str)


def batch_inspectAPP_android(path):
    DL_models = {}
    save_json = r'../data/android_models_ase.json'
    org_models = {}
    for dir in os.listdir(path):
        app_path = os.path.join(path, dir)
        print(app_path)
        inspectAPP(app_path, DL_models)

    with open(save_json, 'r', encoding='utf8') as f:
        org_models = json.load(f)

    if org_models:
        DL_models = org_models | DL_models
    json_str = json.dumps(DL_models)
    with open(save_json, 'w', encoding='utf8') as f2:
        f2.write(json_str)


if __name__ == '__main__':
    src = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/Sicoob.app'

    path = r'/Users/hhuu0025/Downloads/ipa_dataset/zips'
    #batch_inspectAPP(path)

    path2 = r'/home/suyu/Documents/dataset/Suyu/data//recompiled_tf_apks'
    batch_inspectAPP_android(path2)
