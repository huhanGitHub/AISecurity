import json
import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher

DL_model_fields = ['.tflite', '.model', '.mlmodelc', '.mlmodel', '.pt', '.pb', '.h5', '.tfl', '.cfg']
DL_model_fields_count = [0,0,0,0,0,0,0,0,0]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()





def match_android_ios_app_with_models():
    path1 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_models_final.json'
    path2 = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/ios_models_final.json'
    save = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/android_IOS_models_final.json'
    same_app_models = {}
    android_app_models = json.load(open(path1, 'r', encoding='utf8'))
    ios_app_models = json.load(open(path2, 'r', encoding='utf8'))
    a = 0
    b = 0
    c = 0
    for k1, v1 in android_app_models.items():
        k1 = k1.lower()
        for k2, v2 in ios_app_models.items():
            k2_name = k2
            k1 = k1.lower()
            k2_name = k2_name.lower()
            similarity = similar(k1, k2_name)
            if k1 in k2_name or k2_name in k1:
                similarity = 1

            if similarity > 0.7:
                models = []
                print(k1 + '---' + k2_name)
                models.append('android')
                models.extend(v1)
                models.append('ios')
                ios_models = v2
                ios_models = [str(i).lower() for i in ios_models]
                an_models = [str(i).lower() for i in v1]
                models.extend(v2)

                same_models = set(an_models) & set(ios_models)
                if len(same_models) == 0:
                    # print('no same')
                    models.append('no same')
                    a += 1
                elif len(same_models) == len(v1) and len(same_models) == len(ios_models):
                    # print('all the same')
                    models.append('all same')
                    print(k1)
                    b += 1
                else:
                    # print('partly same')
                    models.append('partly same')
                    c += 1

                key = '(' + k1 + ',' + k2_name + ')'
                same_app_models[key] = models


    print('no same: ' + str(a) + ' all the same: ' + str(b) + ' partly same: ' + str(c))

    with open(save, 'w', encoding='utf8') as f:
        print(len(same_app_models.keys()))
        f.write(json.dumps(same_app_models, indent=4))


if __name__ == '__main__':
    # generate_Android_Ios_json()
    # count_android_apps()

    all_path = r'../data/android_ios_model_pairs_all.txt'
    same_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/sameDLsameApp'
    # paired_model_analysis(all_path)
    # paired_model_analysis(same_path)

    # model_count_analysis()

    match_android_ios_app_with_models()
