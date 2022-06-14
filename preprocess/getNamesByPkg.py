from bs4 import BeautifulSoup
import requests
import json
import os
from inspectIPA import DL_model_fields


def findNamesFromApkpure(pkg):
    url = 'https://play.google.com/store/search?q=' + pkg + '&c=apps'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
               }
    get_html = requests.get(url, headers=headers)
    # print(get_html.text)
    soup = BeautifulSoup(get_html.text, 'lxml')
    apps_html = soup.find_all('span', {"class": "DdYX5"})

    apps = []
    for app_html in apps_html:
        # print(str(app.text).strip())
        value = str(app_html.text).strip()
        value = value.encode().decode('unicode-escape')
        apps.append(value)

    return apps


def androidIosPair():
    csvFile = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/DL Apps-ASE2022 - DL App Summary.csv'
    saveFile = r'../data/pkgs.txt'
    with open(csvFile, 'r', encoding='utf8') as f:
        lines = f.readlines()
        lines = lines[1:]
        pkgs = []
        for line in lines:
            pkg = line.split(',')[0]
            pkgs.append(pkg)

    all_apps = []
    for pkg in pkgs:
        app = findNamesFromApkpure(pkg)

        # select top 2 apps
        if len(app) > 0:
            app = app[0]
            all_apps.append(app)

    # json_results = json.dumps(all_apps)

    with open(saveFile, 'a', encoding='utf8') as f2:
        for all_app in all_apps:
            f2.write(all_app + '\n')


def get_app_name_pkg():
    # directory = r'/home/suyu/Documents/dataset/Suyu/data//recompiled_tf_apks'
    directory = r'/Users/hhuu0025/PycharmProjects/guidedExplorer/data/recompiled_apks'
    save_file = r'../data/android_apps_with_models.txt'
    failed_pkg = r'../data/failed_android_pkg_with_models.txt'
    valid_apps = {}
    valid_app_packages = []
    for apk in os.listdir(directory):
        apk_path = os.path.join(directory, apk)
        skip_status = True
        models = []
        for root, dirs, files in os.walk(apk_path):
            # filter models
            for file in files:
                suffix = file[str(file).rfind('.'):]
                if suffix in DL_model_fields:
                    print('found DL model')
                    models.append(file)
                    skip_status = False

        if skip_status:
            continue

        for root, dirs, files in os.walk(apk_path):
            # get the app name from decompiled apk source files
            for dir in dirs:
                # print(dir)
                if dir == 'values':
                    try:
                        # strings = dir_path + '//res/values/strings.xml'
                        strings = os.path.join(root, dir, 'strings.xml')
                        with open(strings, 'r') as f:
                            # lines = f.readlines()
                            # content = ' '.join(lines)
                            content = f.read()
                            soup = BeautifulSoup(content, 'lxml')
                            app_name = soup.find('string', {"name": "app_name"})
                            # if app_name is None:
                            #     print('no app name ' + apk)
                            #     continue
                            name = app_name.text
                            print(apk + ' ' + name)
                            valid_apps[name] = models
                    except Exception as e:
                        print('exception ' + apk)
                        if not skip_status:
                            valid_app_packages.append(apk)

    with open(save_file, 'w', encoding='utf8') as f2:
        print('total apps: ' + str(len(valid_apps.keys())))
        json_valid = json.dumps(valid_apps)
        f2.write(json_valid)

    with open(failed_pkg, 'w', encoding='utf8') as f3:
        for pkg in valid_app_packages:
            f3.write(pkg + '\n')


if __name__ == '__main__':
    pkg = 'com.skype.raider'
    # findNamesFromApkpure(pkg)

    # androidIosPair()

    get_app_name_pkg()