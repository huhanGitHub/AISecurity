import os
import json
from plistlib import load, FMT_XML
DL_model_fields = ['.tflite', '.model', '.mlmodelc', '.mlmodel', '.pt', '.pb', '.h5', '.tfl', '.cfg', '.caffemodel', '.feathermodel', '.pkl', '.chainermodel']
DL_model_fields_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
from ipatoolDownloader import ipatoolDownloader
import zipfile
import shutil


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
        # plist_path = os.path.join(src, 'iTunesMetadata.plist')
        with open(plist_path, 'rb') as f:
            plist_dict = load(f, fmt=FMT_XML)
            itemName = plist_dict['itemName']
            bundleDisplayName = plist_dict['bundleDisplayName']
            # last one is the app name
            models.append(bundleDisplayName)
            models.append(itemName)
        DL_models[src] = models


def inspectAPP_android(src, DL_models):
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
        app_name = src[str(src).rindex('/') +1: ]
        models.append(app_name)
        models.append(app_name)
        DL_models[src] = models



def batch_inspectAPP(path):
    DL_models = {}
    save_json = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/ios_models_top.json'
    org_save_json = {}
    app_count = 0
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if str(dir).endswith('.app'):
                app_count += 1
                app_path = os.path.join(root, dir)
                print(str(app_count) + ' ' + app_path)
                inspectAPP(app_path, DL_models)

    json_str = json.dumps(DL_models, indent=4)

    print('total apps with models: ' + str(len(DL_models.keys())))
    for index, i in enumerate(DL_model_fields_count):
        print(DL_model_fields[index] + ': ' + str(DL_model_fields_count[index]))

    with open(save_json, 'w', encoding='utf8') as f2:
        f2.write(json_str)


def batch_inspectAPP_android(path):
    DL_models = {}
    save_json = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_models_top.json'
    org_models = {}
    for dir in os.listdir(path):
        app_path = os.path.join(path, dir)
        print(app_path)
        inspectAPP_android(app_path, DL_models)

    # if os.path.exists(save_json):
    #     with open(save_json, 'r', encoding='utf8') as f:
    #         org_models = json.load(f)
    #
    #     if org_models:
    #         DL_models = org_models | DL_models
    json_str = json.dumps(DL_models, indent=4)

    print('total apps with models: ' + str(len(DL_models.keys())))
    print(DL_model_fields_count)

    with open(save_json, 'w', encoding='utf8') as f2:
        f2.write(json_str)


def downloadInspectFilter(app, DL_models, save_dir=r'../data/topAppleApps'):
    downloadStatus, output_file = ipatoolDownloader(app, save_dir)
    if not downloadStatus:
        print('download ' + app + ' failed')
        return False

    IPA_path = output_file
    # unzip ipa
    with zipfile.ZipFile(IPA_path, 'r') as zip_ref:
        zip_ref.extractall(IPA_path[:-4])

    # inspect dl models
    app_DL_models = []
    inspectAPP(IPA_path, app_DL_models)
    if len(app_DL_models) != 0:
        print('find DL model in ' + app)
        DL_models.extend(app_DL_models)

    else:
        print('cannot find DL model in ' + app + ' , delete')
        shutil.rmtree(IPA_path[:-4])
        os.remove(IPA_path)

    return True


def batch_downloadInspectFilter(app_list):
    save_dir = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps'
    save_json = r'../data/android_models_top.json'
    DL_models = []
    # log 0: downloaded, checked; 1: download fail
    download_log = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/top_apps.log'

    apps = open(app_list, 'r', encoding='utf8').readlines()
    apps = [i.replace('\n', '').strip() for i in apps]
    count = 0
    begin = 255
    max_download = 100

    with open(download_log, 'a', encoding='utf8') as log:
        for index, app in enumerate(apps):
            app = app.replace(' ', '_')
            app = app.replace('&', '7')
            if index < begin:
                continue

            if count >= max_download:
                print('download ' + str(max_download) + ' , stop')
                return

            if 'category: ' in app:
                continue

            status = downloadInspectFilter(app, DL_models, save_dir)
            if status:
                count += 1
                log.write(app + '---' + str(1) + '\n')
                print('count: ' + str(count))
            else:
                log.write(app + '---' + str(0) + '\n')

    json_str = json.dumps(DL_models)
    with open(save_json, 'w', encoding='utf8') as f2:
        f2.write(json_str)


def read_json2list(top_app_list):
    apps = []
    app_dict = json.load(open(top_app_list, 'r', encoding='utf8'))
    for k, v in app_dict.items():
        app = v[-1]
        apps.append(app)

    save_file = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/iosAppModels.txt'
    with open(save_file, 'a', encoding='utf8') as f:
        for app in apps:
            f.write(app + '\n')


if __name__ == '__main__':
    src = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/Sicoob.app'

    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/ipas_all'
    # batch_inspectAPP(path)

    path2 = r'/Volumes/daneimiji/AndroidApps/topRatedApps/extracted/'
    batch_inspectAPP_android(path2)
    # batch_inspectAPP(path2)

    top_app_list = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/topAppleApps.txt'
    # batch_downloadInspectFilter(top_app_list)

    # read_json2list(r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/ios_models_top.json')
