import urllib.request

from bs4 import BeautifulSoup
import os
import requests
import re
from urllib.request import urlopen, Request
import zipfile


def searchByName_apkpure(app_name):
    # replace ' ' with '+'
    try:
        app_name = app_name.replace(' ', '+')
        server_addr = 'https://apkpure.com'
        url = 'https://apkpure.com/search?q=' + app_name + '&t=app'
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=headers)
        # search app
        get_html = urlopen(req).read()
        get_html = get_html.decode('utf-8')
        soup = BeautifulSoup(get_html, 'html.parser')
        apps = soup.find_all('a', {'title': re.compile(' APK$')})

        href = apps[0]['href']
        url2 = server_addr + href + '/versions'
        # print(full_href)

        # click first app, and go to its version page
        req2 = Request(url2, headers=headers)
        get_html2 = urlopen(req2).read()
        get_html2 = get_html2.decode('utf-8')
        soup2 = BeautifulSoup(get_html2, 'html.parser')
        ul = soup2.find('ul', {"class": "ver-wrap"})
        versions = ul.find_all('li')
        url3 = ''
        for version in versions:
            xapk = version.find('span', {"class": "ver-item-t ver-xapk"})
            # download 'apk'
            if xapk is None:
                apk_link = version.find('a')['href']
                url3 = server_addr + apk_link
                break

        # find click download
        req3 = Request(url3, headers=headers)
        get_html3 = urlopen(req3).read()
        get_html3 = get_html3.decode('utf-8')
        soup3 = BeautifulSoup(get_html3, 'html.parser')
        download_link = soup3.find('a', {"id": "download_link"})['href']
    except Exception as e:
        print(str(e))
        return False

    return download_link


def url_downloader(url, app_name, save_dir):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        save_path = os.path.join(save_dir, app_name + '.zip')
        if os.path.exists(save_path):
            print(app_name+' has been downloaded')
            return save_path
        response = urlopen(req).read()
        open(save_path, 'wb').write(response)
    except Exception as e:
        print(str(e))
        return False

    return save_path


def zip_extractor(zip_path, save_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # get modified app name
        modified_app = zip_path[str(zip_path).rindex('/') + 1:-4]
        extracted_app = os.path.join(save_dir, modified_app)
        # remove .zip
        zip_ref.extractall(extracted_app)


def find_android_app(app_name, save_dir):
    url = searchByName_apkpure(app_name)
    if url is False:
        return False
    zip_path = url_downloader(url, app_name, save_dir)
    if zip_path is False:
        return False
    extracted_app_dir = save_dir[:-4] + 'extracted'
    zip_extractor(zip_path, extracted_app_dir)
    return True


def batch_find_android_app(app_list, save_dir):
    apps = []
    with open(app_list, 'r', encoding='utf8') as f:
        apps = f.readlines()
        apps = [i.replace('\n', '') for i in apps]

    failed_app_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/failed_Android_apps.txt'
    with open(failed_app_path, 'a', encoding='utf8') as f1:
        for index, app in enumerate(apps):
            status = find_android_app(app, save_dir)
            if not status:
                f1.write(app + '\n')
            print(str(status) + ' ' + app + ' ' + str(index))


if __name__ == '__main__':
    app_name = 'Webex Meetings'
    save_dir = r'/Volumes/daneimiji/AndroidApps/topRatedApps/zips'
    # find_android_app(app_name, save_dir)
    # searchByName_apkpure(app_name)
    app_list = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/iosAppModels.txt'
    batch_find_android_app(app_list, save_dir)