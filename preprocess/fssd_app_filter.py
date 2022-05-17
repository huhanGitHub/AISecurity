import os
from bs4 import BeautifulSoup


def fssd_filter():
    # directory = r'/home/suyu/Documents/dataset/Suyu/data//recompiled_tf_apks'
    directory = r'/Users/hhuu0025/PycharmProjects/guidedExplorer/data/recompiled_apks'
    save_file = r'../data/valid_apps.txt'
    valid_apps = []
    valid_app_packages = []
    for apk in os.listdir(directory):
        apk_path = os.path.join(directory, apk)
        for root, dirs, files in os.walk(apk_path):
            # filter fssd
            skip_status = False
            for file in files:
                if 'fssd' in file:
                    print(apk + ' ' + file + ' skip')
                    skip_status = True
                    break

            if skip_status:
                break

            # get the app name from decompiled apk source files
            for dir in dirs:
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
                            print(app_name.text)
                            valid_apps.append(app_name.text)
                    except Exception as e:
                        print('exception ' + apk)
                        valid_app_packages.append(apk)

    with open(save_file, 'w', encoding='utf8') as f2:
        for app_name in valid_apps:
            f2.write(app_name + '\n')

        f2.write('\n\n\napp package names \n')
        for pkg in valid_app_packages:
            f2.write(pkg + '\n')


if __name__ == '__main__':
    fssd_filter()