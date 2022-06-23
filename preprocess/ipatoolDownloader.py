import json
import subprocess


# note that you must login via the terminal before download ipas. The login token will expire after about 1 hour.
def ipatoolDownloader(app, save_dir=r'../data/ipas_all/'):
    app = app.replace(' ', '\ ')
    cmd1 = 'ipatool search --limit 1 ' + app
    p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    r1 = p1.stdout.read()
    if 'Found' not in r1:
        return False
    try:
        pkg = r1[r1.rindex(': ') + 2: r1.rindex(' (')].strip()
        print(pkg)

        cmd2 = 'ipatool purchase --bundle-identifier ' + pkg
        p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        r2 = p2.stdout.read()
        if 'Done' not in r2:
            print('purchased before or purchase fail, skip')
            return False

        # save ipa files to 'app'.zip
        cmd3 = 'ipatool download --bundle-identifier ' + pkg + ' -o ' + save_dir + app + '.zip'
        p3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        r3 = p3.stdout.read()
        if 'Done' not in r3:
            return False
    except ValueError as e:
        print(str(e) + ' ' + r1)

    return True


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
            status = ipatoolDownloader(app)
            if status:
                count += 1
            print('------------IPA downloader: ' + k + ' ' + str(status) + ' ' + str(count)+'\n')


def batch_ipatoolDownloader_txt(txt_file, save_dir):
    maximum = 300

    begin = 0

    # load all apps from txt
    apps = open(txt_file, 'r', encoding='utf8').readlines()
    apps = [i.replace('\n', '') for i in apps]
    count = 0
    for i, app in enumerate(apps):
        if count < begin:
            count += 1
            continue

        if count >= begin + maximum:
            break
        else:
            if app.startswith('category: '):
                continue
            status = ipatoolDownloader(app, save_dir)
            if status:
                count += 1
            print('------------IPA downloader: ' + str(i) + ' ' + str(status) + ' ' + str(count)+'\n')


if __name__ == '__main__':
    app = 'Google Duo'
    # ipatoolDownloader(app)

    json_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_ios_app_pairs_all.json'
    batch_ipatoolDownloader(json_path)

    txt_path = r'../data/topAppleApps/topAppleApps.txt'
    save_dir = r'../data/topAppleApps/'
    batch_ipatoolDownloader_txt(txt_path, save_dir)
