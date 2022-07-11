import json
import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher

DL_model_fields = ['.tflite', '.model', '.mlmodelc', '.mlmodel', '.pt', '.pb', '.h5', '.tfl', '.cfg']
DL_model_fields_count = [0,0,0,0,0,0,0,0,0]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def generate_Android_Ios_json():
    models = {}
    android_models = []
    # parse android csv

    # find corresponding name from pkg
    pkg_name_pair_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/pkgs.json'
    pkg_name_pair = json.load(open(pkg_name_pair_path, 'r', encoding='utf8'))

    # android_models_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/androidDLmodels.csv'
    # with open(android_models_path, 'r', encoding='utf8') as f:
    #     lines = f.readlines()[1:]
    #     for line in lines:
    #         line = line.replace('\n', '').split(',')
    #         pkg = line[0]
    #         name = pkg_name_pair.get(pkg, 0)
    #         if name == 0:
    #             continue
    #         models = line[-1]
    #         if ';' in models:
    #             models = models.split(';')
    #         else:
    #             models = [models]
    #         android_models.append([name, models])

    android_models_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_apps_with_models_all.json'
    android_models_dict = json.load(open(android_models_path, 'r', encoding='utf8'))


    # parse ios models
    ios_models_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/IOS_models_all.json'
    ios_models_dict = json.load(open(ios_models_path, 'r', encoding='utf8'))
    ios_models = []

    # count

    for k, v in android_models_dict.items():
        for vv in v:
            suffix = vv[str(vv).rfind('.'):]
            index = DL_model_fields.index(suffix)
            if index != -1:
                DL_model_fields_count[index] += 1

    # print(DL_model_fields_count)

    result_dict = {}
    for k, v in ios_models_dict.items():
        app = k[str(k).rindex('/') + 1: str(k).rindex('.app')]
        # ios_models.append([app, v])
        # similarities = [similar(i[0], app) for i in android_models]
        # max_index = similarities.index(max(similarities))
        # print(str(similarities[max_index]) + ' ' + android_models[max_index][0] + ' | ' + app)
        # a_v = android_models[max_index][1]
        #
        # for i in v:
        #     for j in a_v:
        #         if similar(i, j) > 0.7:
        #             print(i)

        # line = app + ' | ' + android_models[max_index]
        pair_save_path = r'../data/android_ios_model_pairs_all.txt'
        with open(pair_save_path, 'a', encoding='utf8') as f3:
            for i in v:
                for kk, vv in android_models_dict.items():
                    for ii in vv:
                        if similar(ii, i) > 0.7:
                            # if 'fssd' in ii:
                            #     continue
                            subline1 = str(similar(ii, i)) + '---' + i + '---' + ii

                            #apk = kk[str(kk).rindex('/') + 1: str(kk).rindex('.apk')]
                            apk = kk
                            subline2 = app + '---' + apk
                            if similar(apk, app) > 0.7:
                                print(subline1 + '---' + subline2)
                            # ios---android
                            f3.write(subline1 + '---' + subline2 + '\n')


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



def model_count_analysis():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/IOS_models_all.json'
    android_models_dict = json.load(open(path, 'r', encoding='utf8'))
    ratio = []

    for k, v in android_models_dict.items():
        if len(v) > 50:
            continue
        ratio.append(len(v) - 2)

    ratio = np.array(ratio)
    fig = plt.figure(figsize=(10, 7))

    # Creating plot
    plt.boxplot(ratio)

    # show plot
    plt.show()


def match_android_ios_app_with_models():
    path1 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_apps_with_models_all.json'
    path2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/IOS_models_all.json'
    save = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_IOS_models_all.json'
    same_app_models = {}
    android_app_models = json.load(open(path1, 'r', encoding='utf8'))
    ios_app_models = json.load(open(path2, 'r', encoding='utf8'))
    a=0
    b=0
    c=0
    for k1, v1 in android_app_models.items():
        for k2, v2 in ios_app_models.items():
            k2_name = v2[-2]
            similarity = similar(k1, k2_name)
            if similarity > 0.8:
                models = []
                print(k1 + '---' + k2_name)
                models.append('android')
                models.extend(v1)
                models.append('ios')
                ios_models = v2[:-2]
                ios_models = [str(i).lower() for i in ios_models]
                an_models = [str(i).lower() for i in v1]
                models.extend(v2[:-2])

                same_models = set(an_models) & set(ios_models)
                if len(same_models) == 0:
                    print('no same')
                    models.append('no same')
                    a += 1
                elif len(same_models) == len(v1) and len(same_models) == len(ios_models):
                    print('all the same')
                    models.append('all same')
                    print(k1)
                    b += 1
                else:
                    print('partly same')
                    models.append('partly same')
                    c += 1

                same_app_models[k1] = models

    print(a, b, c)

    with open(save, 'a', encoding='utf8') as f:
        f.write(json.dumps(same_app_models, indent=4))


if __name__ == '__main__':
    # generate_Android_Ios_json()
    # count_android_apps()

    all_path = r'../data/android_ios_model_pairs_all.txt'
    same_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/sameDLsameApp'
    # paired_model_analysis(all_path)
    # paired_model_analysis(same_path)

    #model_count_analysis()

    match_android_ios_app_with_models()