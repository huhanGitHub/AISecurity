import os
import json
from plistlib import load, FMT_XML
DL_model_fields = ['.tflite', '.model', '.mlmodelc', '.mlmodel', '.pt', '.pb', '.h5', '.tfl', '.cfg', '.caffemodel', '.feathermodel', '.pkl', '.chainermodel']
DL_model_fields_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def inspectAPP(src, DL_models):
    models = []
    for root, dirs, files in os.walk(src):
        for file in files:
            suffix = file[str(file).rfind('.'):]
            if suffix in DL_model_fields:
                print('found DL model')
                index = DL_model_fields.index(suffix)
                models.append(file)
                DL_model_fields_count[index] += 1

        for dir in dirs:
            suffix = dir[str(dir).rfind('.'):]
            if suffix in DL_model_fields:
                print('found DL model')
                models.append(dir)
                index = DL_model_fields.index(suffix)
                DL_model_fields_count[index] += 1

    if len(models) > 0:
        # find plist to get app name
        plist_path = os.path.join(src[:src.rindex('Payload')], 'iTunesMetadata.plist')
        with open(plist_path, 'rb') as f:
            plist_dict = load(f, fmt=FMT_XML)
            itemName = plist_dict['itemName']
            bundleDisplayName = plist_dict['bundleDisplayName']
            # last one is the app name
            models.append(bundleDisplayName)
            models.append(itemName)
        DL_models[src] = models


def batch_inspectAPP(path):
    DL_models = {}
    save_json = r'../data/IOS_models_all.json'
    org_save_json = {}
    app_count = 0
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if str(dir).endswith('.app'):
                app_count += 1
                app_path = os.path.join(root, dir)
                print(str(app_count) + ' ' + app_path)
                inspectAPP(app_path, DL_models)

    json_str = json.dumps(DL_models)

    print('total apps with models: ' + str(len(DL_models.keys())))
    print(DL_model_fields_count)

    with open(save_json, 'w', encoding='utf8') as f2:
        f2.write(json_str)


def batch_inspectAPP_android(path):
    DL_models = {}
    save_json = r'../data/android_models_all.json'
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

    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/ipas_all'
    batch_inspectAPP(path)

    path2 = r'/home/suyu/Documents/dataset/Suyu/data//recompiled_tf_apks'
    # batch_inspectAPP_android(path2)
