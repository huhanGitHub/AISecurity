import os
import json
skip_list = ['.DS_Store']
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import numpy as np

DL_model_fields = ['.tflite', '.model', '.mlmodelc', '.mlmodel', '.pt', '.pb', '.h5', '.tfl', '.cfg', '.caffemodel', '.feathermodel', '.pkl', '.chainermodel']

DL_model_fields_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def rename(path):
    for file in os.listdir(path):
        if file in skip_list:
            continue
        old_file_path = os.path.join(path, file)
        if '.zip' not in file:
            new_file_path = os.path.join(path, file + '.zip')
            os.rename(old_file_path, new_file_path)


def merge_models(json1, json2):
    save_json = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/ios_models_final.json'
    ios_app_list = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/ios_apps_model_simpilified_final.txt'
    data1 = json.load(open(json1, 'r', encoding='utf8'))
    data2 = json.load(open(json2, 'r', encoding='utf8'))
    merge = {}

    for k1, v1 in data1.items():
        app = v1[-1]
        models = v1[:-2]
        cur_keys = merge.keys()
        if app not in cur_keys:
            merge[app] = models
        else:
            cur_models = merge.get(app)[:-2]
            all_models = set(cur_models.extend(models))
            merge[app] = all_models

    for k2, v2 in data2.items():
        app = v2[-1]
        models = v2[:-2]
        cur_keys = merge.keys()
        if app not in cur_keys:
            merge[app] = models
        else:
            cur_models = merge.get(app)[:-2]
            for i in models:
                if i not in cur_models:
                    cur_models.append(i)
            merge[app] = cur_models

    with open(save_json, 'w', encoding='utf8') as f:
        f.write(json.dumps(merge, indent=4))
    with open(ios_app_list, 'w', encoding='utf8') as f2:
        for app in merge.keys():
            f2.write(app + '\n')


def merge_models_andoird(json1, json2):
    save_json = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_models_final.json'
    android_app_list = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_apps_model_simpilified_final.txt'
    data1 = json.load(open(json1, 'r', encoding='utf8'))
    data2 = json.load(open(json2, 'r', encoding='utf8'))
    merge = {}

    for k1, v1 in data1.items():
        app = v1[-2]
        models = v1[:-2]
        cur_keys = merge.keys()
        if app not in cur_keys:
            merge[app] = models
        else:
            cur_models = merge.get(app)[:-2]
            all_models = set(cur_models.extend(models))
            merge[app] = all_models

    for k2, v2 in data2.items():
        app = k2
        models = v2
        cur_keys = merge.keys()
        if app not in cur_keys:
            merge[app] = models
        else:
            cur_models = merge.get(app)[:-2]
            for i in models:
                if i not in cur_models:
                    cur_models.append(i)
            merge[app] = cur_models

    print(len(merge.keys()))
    with open(save_json, 'w', encoding='utf8') as f:
        f.write(json.dumps(merge, indent=4))
    with open(android_app_list, 'w', encoding='utf8') as f2:
        for app in merge.keys():
            f2.write(app + '\n')


def find_model_pair(model_json):
    models = json.load(open(model_json, 'r', encoding='utf8'))
    save_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/sameAppSameModel.txt'
    with open(save_path, 'a', encoding='utf8') as f:
        for k, v in models.items():
            android = []
            ios = []
            tag = 0
            for index, model in enumerate(v):
                if model == 'ios':
                    tag = index
            android = v[1:tag]
            ios = v[tag+1: -1]
            for i in android:
                for j in ios:
                    ii = str(i).lower()
                    jj = str(j).lower()
                    ii = ii[:ii.rindex('.')-1]
                    jj = jj[:jj.rindex('.') - 1]
                    similarity = similar(ii, jj)
                    if similarity > 0.9:
                        line = k + ' , ' + i + ' , ' + j + ' , ' + str(similarity)
                        f.write(line + '\n')


def merge():
    json1 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/IOS_models_all.json'
    json2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/ios_models_top.json'
    # merge_models(json1, json2)

    json3 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_models_top.json'
    json4 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_apps_with_models_all.json'
    merge_models_andoird(json3, json4)


def count_android_apps():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_models_ase.json'
    android_models_dict = json.load(open(path, 'r', encoding='utf8'))
    print(len(android_models_dict.keys()))


def paired_model_analysis(path):
    print(path)
    models = {}
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            strings = line.split('---')
            ios_model = strings[1]
            count = models.get(ios_model, 0)
            if count == 0:
                models[ios_model] = 1
            else:
                models[ios_model] = count + 1

            an_model = strings[2]
            count = models.get(an_model, 0)
            if count == 0:
                models[an_model] = 1
            else:
                models[an_model] = count + 1

    models = {k: v for k, v in sorted(models.items(), key=lambda item: item[1], reverse=True)}
    for k, v in models.items():
        print(k + ' ' + str(v))


def model_boxplot():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_models_final.json'
    android_models_dict = json.load(open(path, 'r', encoding='utf8'))
    ratio = []
    count = 0
    for k, v in android_models_dict.items():
        if len(v) > 20:
            count += 1
            continue
        ratio.append(len(v))

    ratio = np.array(ratio)
    # fig = plt.figure(figsize=(10, 7))

    # Creating plot
    fig, ax = plt.subplots()
    bp = ax.boxplot(ratio, showmeans=True)
    mean = ratio.mean()

    for i, line in enumerate(bp['medians']):
        x, y = line.get_xydata()[1]
        text = 'median={:.2f}'.format(y)
        ax.annotate(text, xy=(x, y))
        text2 = 'mean={:.2f}'.format(mean)
        ax.annotate(text2, xy= (x, mean))

    # show plot
    plt.show()
    print(count)


def model_framework_analysis():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_models_final.json'
    ios_models_dict = json.load(open(path, 'r', encoding='utf8'))

    for k, v in ios_models_dict.items():
        for model in v:
            suffix = model[model.rindex('.'):]
            index = DL_model_fields.index(suffix)
            DL_model_fields_count[index] += 1

    y = np.array(DL_model_fields_count)

    plt.pie(y, labels=DL_model_fields)
    #plt.legend(DL_model_fields, loc='center right')
    plt.show()

    print('total models: ' + str(sum(DL_model_fields_count)))
    print(DL_model_fields_count)


def sameModelsameApp():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/sameAppSameModel.txt'
    pairs = open(path, 'r', encoding='utf8').readlines()
    pairs = [i.replace('\n', '') for i in pairs]
    app_pairs = {}
    suffixes = {}
    for pair in pairs:
        app_pair, model1, model2, similarity = pair.split(' , ')
        i = app_pairs.get(app_pair, 0)
        app_pairs[app_pair] = i + 1
        model1_suffix = model1[model1.rindex('.'):]
        model2_suffix = model2[model2.rindex('.'):]
        suffix = model1_suffix + '-->' + model2_suffix
        j = suffixes.get(suffix, 0)
        suffixes[suffix] = j + 1

    app_pairs = {k: v for k, v in sorted(app_pairs.items(), key=lambda item: item[1], reverse=True)}
    suffixes = {k: v for k, v in sorted(suffixes.items(), key=lambda item: item[1], reverse=True)}

    path1 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/sameAppSameModel/app_pairs.txt'
    path2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/sameAppSameModel/model_conversion.txt'
    titles = []
    values = []
    with open(path1, 'w', encoding='utf8') as f1, open(path2, 'w', encoding='utf8') as f2:
        for k1, v1 in app_pairs.items():
            f1.write(k1 + ' ' + str(v1) + '\n')
        for k2, v2 in suffixes.items():
            f2.write(k2 + ' ' + str(v2) + '\n')
            titles.append(k2)
            values.append(v2)

    y = np.array(values)

    plt.pie(y, labels=titles)
    #plt.legend(DL_model_fields, loc='center right')
    plt.show()


if __name__ == '__main__':
    model_json = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_IOS_models_final.json'
    # find_model_pair(model_json)
    # model_boxplot()
    # model_framework_analysis()
    sameModelsameApp()