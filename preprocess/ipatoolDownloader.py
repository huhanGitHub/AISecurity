import json
import subprocess


# note that you must login via the terminal before download ipas. The login token will expire after about 1 hour.
def ipatoolDownloader(app):
    app = app.replace(' ', '\ ')
    cmd1 = 'ipatool search --limit 1 ' + app
    p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    r1 = p1.stdout.read()
    if 'Found' not in r1:
        return False
    try:
        # '==> ℹ️	[Info] Searching for \'StuffThatWorks\' using the \'US\' store front...
        # ==> ℹ️	[Info] Found 1 result:
        # 1. StuffThatWorks: co.StuffThatWorks (0.8).
        # '
        pkg = r1[r1.rindex(': ') + 2: r1.rindex(' (')].strip()
        print(pkg)

        cmd2 = 'ipatool purchase --bundle-identifier ' + pkg
        p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        r2 = p2.stdout.read()
        if 'Done' not in r2:
            # return False
            print('purchased before')

        cmd3 = 'ipatool download --bundle-identifier ' + pkg + ' -o ' + '../data/ipas_ase/'
        p3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        r3 = p3.stdout.read()
        if 'Done' not in r3:
            return False
    except ValueError as e:
        print(str(e) + ' ' + r1)

    return True


def batch_ipatoolDownloader(json_file):
    maximum = 50

    begin = 18

    # load all apps from json
    apps_json = json.load(open(json_file, 'r', encoding='utf8'))
    count = 0
    for k, v in apps_json.items():
        if count < begin:
            count += 1
            continue

        if count >= maximum:
            break
        else:
            count += 1
        app = v[0]
        status = ipatoolDownloader(app)
        print('------------IPA downloader: ' + k + ' ' + str(status) + ' ' + str(count)+'\n')


if __name__ == '__main__':
    app = 'Google Duo'
    # ipatoolDownloader(app)

    json_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_ios_app_pairs_ase.json'
    batch_ipatoolDownloader(json_path)