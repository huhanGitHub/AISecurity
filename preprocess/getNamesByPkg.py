from bs4 import BeautifulSoup
import requests
import json


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


if __name__ == '__main__':
    pkg = 'com.skype.raider'
    # findNamesFromApkpure(pkg)

    androidIosPair()