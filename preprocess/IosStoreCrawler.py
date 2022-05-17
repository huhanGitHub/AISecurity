import re
from bs4 import BeautifulSoup
import requests
import json


# https://www.apple.com/au/search/image?sel=explore&src=globalnav&tab=explore&page=1


def crawler_app_store(target):
    url = 'https://www.apple.com/au/search/' + target + '?sel=explore&src=globalnav&tab=explore&page=1'
    get_html = requests.get(url)
    # print(get_html.text)
    soup = BeautifulSoup(get_html.text, 'lxml')
    apps = soup.find_all('h2', {"class": "rf-serp-productname"})

    app_ios = []
    for app in apps:
        # print(str(app.text).strip())
        app_ios.append(str(app.text).strip())

    # select top 2 apps
    app_ios = app_ios if len(app_ios) <= 2 else app_ios[:2]
    result = {target: app_ios}

    return result


def batch_crawler_app_store(targets, save_path):
    results = {}
    for target in targets:
        result = crawler_app_store(target)
        results.update(result)

    json_results = json.dumps(results)

    with open(save_path, 'w', encoding='utf8') as f:
        f.write(json_results)


if __name__ == '__main__':
    targets = ['wechat', 'image', 'xxxxxx']
    save_path = r'../data/android_ios_app_pairs.json'
    batch_crawler_app_store(targets, save_path)
