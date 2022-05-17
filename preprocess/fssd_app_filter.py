import os
from bs4 import BeautifulSoup


def fssd_filter():
    directory = r'/home/suyu/Documents/dataset/Suyu/data//recompiled_tf_apks'
    save_file = r'../data/valid_apps.txt'
    valid_apps = []
    for apk in os.listdir(directory):
        apk_path = os.path.join(directory, apk)
        for root, dirs, files in os.walk(apk_path):
            # filter fssd
            for file in files:
                if 'fssd' in file:
                    print(apk + ' ' + file + 'skip')
                    break

            # get the app name from decompiled apk source files
            for dir in dirs:
                if dir == 'values':
                    dir_path = os.path.join(root, dir)
                    strings = dir_path + '//res/values/strings.xml'
                    with open(strings, 'r') as f:
                        lines = f.readlines()
                        content = ' '.join(lines)
                        soup = BeautifulSoup(content, 'lxml')
                        app_name = soup.find_all('string', {"name": "app_name"})
                        print(app_name.text)
                        valid_apps.append(app_name.text)

    with open(save_file, 'r', encoding='utf8') as f2:
        for app_name in valid_apps:
            f2.write(app_name + '\n')


if __name__ == '__main__':
    fssd_filter()