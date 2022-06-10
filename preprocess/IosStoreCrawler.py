import re
from bs4 import BeautifulSoup
import requests
import json


# https://www.apple.com/au/search/image?sel=explore&src=globalnav&tab=explore&page=1


def crawler_app_store(target):
    url = 'https://www.apple.com/search/' + target + '?sel=explore&src=globalnav&tab=explore&page=1'
    get_html = requests.get(url)
    # print(get_html.text)
    soup = BeautifulSoup(get_html.text, 'lxml')
    apps = soup.find_all('h2', {"class": "rf-serp-productname"})

    app_ios = []
    for app in apps:
        # print(str(app.text).strip())
        value = str(app.text).strip()
        value = value.encode().decode('unicode-escape')
        app_ios.append(value)

    # select top 2 apps
    app_ios = app_ios if len(app_ios) <= 2 else app_ios[:2]
    result = None
    if len(app_ios) > 0:
        result = {target: app_ios}

    return result


def batch_crawler_app_store(targets, save_path):
    results = {}
    for target in targets:
        result = crawler_app_store(target)
        if result is not None:
            results.update(result)

    json_results = json.dumps(results)

    with open(save_path, 'w', encoding='utf8') as f:
        f.write(json_results)


def read_app_list(path):
    with open(path, 'r') as f:
        apps = f.readlines()
        apps = [i.replace('\n', '') for i in apps]
        return apps


if __name__ == '__main__':
    targets = ['wechat', 'image', 'xxxxxx']
    save_path = r'../data/android_ios_app_pairs_ase.json'

    # app_list_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/valid_apps.txt'
    app_list_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/pkgs.txt'
    app_list = read_app_list(app_list_path)

    batch_crawler_app_store(app_list, save_path)
