import json

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def generate_Android_Ios_json():
    models = {}
    android_models = []
    # parse android csv

    # find corresponding name from pkg
    pkg_name_pair_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/pkgs.json'
    pkg_name_pair = json.load(open(pkg_name_pair_path, 'r', encoding='utf8'))

    android_models_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/androidDLmodels.csv'
    with open(android_models_path, 'r', encoding='utf8') as f:
        lines = f.readlines()[1:]
        for line in lines:
            line = line.replace('\n', '').split(',')
            pkg = line[0]
            name = pkg_name_pair.get(pkg, 0)
            if name == 0:
                continue
            models = line[-1]
            if ';' in models:
                models = models.split(';')
            else:
                models = [models]
            android_models.append([name, models])

    # parse ios models
    ios_models_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/IOS_models_ase.json'
    ios_models_dict = json.load(open(ios_models_path, 'r', encoding='utf8'))
    ios_models = []

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

        for i in v:
            for j in range(len(android_models)):
                for k in android_models[j][1]:
                    if similar(k, i) > 0.5:
                        print(str(similar(k, i)))
                        print(k + '---' + i)




if __name__ == '__main__':
    generate_Android_Ios_json()