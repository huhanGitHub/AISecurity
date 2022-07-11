import json
import os
import subprocess
from pathlib import Path
import zipfile
import re


# note that you must login via the terminal before download ipas. The login token will expire after about 1 hour.
def ipatoolDownloader(app, save_dir=r'../data/ipas_all/'):
    output_file = False
    app = app.replace(' ', '\ ')
    cmd1 = 'ipatool search --limit 1 ' + app
    p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    r1 = p1.stdout.read()
    if 'Found' not in r1:
        return False, output_file
    try:
        pkg = r1[r1.rindex(': ') + 2: r1.rindex(' (')].strip()
        print(pkg)

        cmd2 = 'ipatool purchase --bundle-identifier ' + pkg
        p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        r2 = p2.stdout.read()
        # if 'Done' not in r2:
        #     print('purchased before or purchase fail, skip')
        #     return False, output_file

        # save ipa files to 'app'.zip
        # app = app.replace('\\ ', '_')
        # app = app.replace('\\.', 'a')
        # app = app.replace(':', 'b')
        # app = app.replace('&', 'c')
        # app = app.replace('/', 'd')
        # app = app.replace(',', 'e')

        # replace all uncommon chars to 'a'
        app = re.sub('[^0-9a-zA-Z]+', 'a', app)

        output_file = save_dir + '/' + app + '.zip'
        path = Path(output_file)
        if path.is_file():
            print('file exists: ' + output_file)
            return True, output_file

        cmd3 = 'ipatool download --bundle-identifier ' + pkg + ' -o ' + output_file
        p3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        r3 = p3.stdout.read()
        if 'Done' not in r3:
            return False, output_file
    except ValueError as e:
        print(str(e) + ' ' + r1)

    return True, output_file


def batch_ipatoolDownloader(json_file):
    maximum = 300

    begin = 0

    # load all apps from json
    apps_json = json.load(open(json_file, 'r', encoding='utf8'))
    count = 0
    for k, v in apps_json.items():
        if count < begin:
            count += 1
            continue

        if count >= begin + maximum:
            break
        else:
            app = v[0]
            status, _ = ipatoolDownloader(app)
            if status:
                count += 1
            print('------------IPA downloader: ' + k + ' ' + str(status) + ' ' + str(count)+'\n')


def batch_ipatoolDownloader_txt(txt_file, save_dir):
    maximum = 300

    begin = 0

    downloaded_app_list = []

    download_log = os.path.join(save_dir, 'apps_list.txt')
    if not os.path.isfile(download_log):
        log = open(download_log, 'w+', encoding='utf8')
    else:
        downloaded_app_list = open(download_log, 'r', encoding='utf8').readlines()
        downloaded_app_list = [i.replace('\n', '') for i in downloaded_app_list]

    extracted_dir = os.path.join(save_dir, 'extracted_ipas')
    if not os.path.isdir(extracted_dir):
        os.mkdir(extracted_dir)

    zip_dir = os.path.join(save_dir, 'zips')
    if not os.path.isdir(zip_dir):
        os.mkdir(zip_dir)

    # load all apps from txt
    apps = open(txt_file, 'r', encoding='utf8').readlines()
    apps = [i.replace('\n', '') for i in apps]
    count = 0

    with open(download_log, 'a', encoding='utf8') as log:
        for i, app in enumerate(apps):
            if count < begin:
                count += 1
                continue

            if app in downloaded_app_list:
                continue

            if count >= begin + maximum:
                break
            else:
                if app.startswith('category: '):
                    continue
                status, output_file = ipatoolDownloader(app, zip_dir)

                if not status:
                    continue

                # extract zip
                with zipfile.ZipFile(output_file, 'r') as zip_ref:
                    # get modified app name
                    modified_app = output_file[str(output_file).rindex('/') + 1:-4]
                    extracted_app = os.path.join(extracted_dir, modified_app)
                    # remove .zip
                    zip_ref.extractall(extracted_app)

                count += 1
                print('------------IPA downloader: ' + str(len(downloaded_app_list) + count) + ' ' + modified_app + ' '
                      + str(status) + ' ' + str(count)+'\n')
                log.write(app + '\n')


if __name__ == '__main__':
    app = 'Google Duo'
    # ipatoolDownloader(app)

    json_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_ios_app_pairs_all.json'
    # batch_ipatoolDownloader(json_path)

    txt_path = r'../data/topAppleApps/topAppleApps.txt'
    # save_dir = r'../data/topAppleApps/'
    save_dir = r'/Volumes/daneimiji/IphoneApps/topRatedApps/'
    batch_ipatoolDownloader_txt(txt_path, save_dir)

