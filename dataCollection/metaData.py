from bs4 import BeautifulSoup
import requests
import json
from modelComparator.compareModelNames import similar
from urllib.request import urlopen, Request


def analysis():
    path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/ios_app_metadata.json'
    metadata = json.load(open(path, 'r', encoding='utf8'))
    scores = []
    sizes = []
    views = []
    cates = {}
    for k, v in metadata.items():
        score = float(v['score'])
        scores.append(score)
        size = v['Size']
        if 'GB' in size:
            size = float(str(size).replace('GB', '').strip()) * 1000
        else:
            size = float(size.replace('MB', '').strip())

        sizes.append(size)
        view = v['number']
        if 'M' in view:
            #view = float(str(view).replace('M', '').strip()) * 1000
            view = 1000
        elif 'K' in view:
            view = float(str(view).replace('K', '').strip())
        else:
            #view = float(view)
            view = 1

        views.append(view)

        cate = v['Category']
        count = cates.get(cate, 0)
        if count == 0:
            cates[cate] = 1
        else:
            cates[cate] = count + 1

    print(scores)
    print(sizes)
    print(views)

    for k, v in cates.items():
        print(k + ' ' + str(v))


def iosMetaDataCrawler():
    ios_app_models_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/IOS_models_all.json'
    ios_app_models = json.load(open(ios_app_models_path, 'r', encoding='utf8'))
    ios_apps = ios_app_models.keys()
    print(len(ios_apps))

    ios_apps_metadata = {}
    for k, v in ios_app_models.items():
        app_name = v[-1]
        bundleDisplayName = v[-2]
        url = 'https://www.apple.com/search/' + bundleDisplayName + '?sel=explore&src=globalnav&tab=explore&page=1'
        get_html = requests.get(url)
        soup = BeautifulSoup(get_html.text, 'html.parser')
        # products = soup.find_all('div', {"class": "rf-serp-product-description"})
        apps = soup.find_all('h2', {"class": "rf-serp-productname"})

        if len(apps) == 0:
            print(app_name + ' skip')
            continue

        app_ios = []
        for app in apps:
            # print(str(app.text).strip())
            value = str(app.text).strip()
            value = value.encode().decode('unicode-escape')
            app_ios.append(value)

        similarities = [similar(app_name, i) for i in app_ios]
        index = similarities.index(max(similarities))
        app_link = soup.find_all('div', {"class": "rf-serp-product-description"})[index].find('a', href=True)
        print(app_link['href'])

        get_html2 = requests.get(app_link['href'])
        soup2 = BeautifulSoup(get_html2.text, 'html.parser')

        ratings = soup2.find('figcaption', {"class": "we-rating-count star-rating__count"})
        ratings_tmp = ratings.text.split(' ')

        atr = {}

        score = ratings_tmp[0]
        number = ratings_tmp[2]
        atr['score'] = score
        atr['number'] = number

        descs = soup2.find_all('div', {"class": "information-list__item l-column small-12 medium-6 large-4 small-valign-top"})
        for desc in descs:
            dt = desc.find('dt').text.replace('\n', '').strip()
            dd = desc.find('dd').text.replace('\n', '').strip()
            atr[dt] = dd
            print('dt: ' + dt + ' dd: ' + dd)

        ios_apps_metadata[app_name] = atr

    save_path = r'../data/ios_app_metadata.json'
    with open(save_path, 'a', encoding='utf8') as f:
        f.write(json.dumps(ios_apps_metadata))


def iosMetaDataCrawler_list():
    ios_app_models_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/ios_apps_model_final.txt'
    ios_apps = open(ios_app_models_path, 'r', encoding='utf8').readlines()
    ios_apps = [i.replace('\n', '') for i in ios_apps]
    print(len(ios_apps))

    ios_apps_metadata = {}
    explored_links = []
    failed_app = []
    for index, app in enumerate(ios_apps):
        if index < 0:
            continue
        org_app = app
        if ':' in app:
            app = app.split(':')[0].strip()
        if ' - ' in app:
            app = app.split(' : ')[0].strip()
        app = app.split(' ')
        if len(app) > 2:
            app = ' '.join(app[:2]).strip()
        else:
            app = ' '.join(app).strip()

        app = app.replace(' ', '-')
        url = 'https://www.apple.com/us/search/' + app + '?src=serp'
        headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'text/html; charset=utf-8'}
        req = Request(url, headers=headers)
        # search app
        try:
            get_html = urlopen(req)
        except UnicodeEncodeError as e:
            print(str(index) + ' ' + app + ' ' + str(e) + ' ' + url)
            continue
        get_html = get_html.read().decode('utf-8')
        # get_html = requests.get(url)
        soup = BeautifulSoup(get_html, 'html.parser')
        # products = soup.find_all('div', {"class": "rf-serp-product-description"})
        apps_tag = soup.find_all('h2', {"class": "rf-serp-productname"})

        if len(apps_tag) == 0:
            print(str(index) + ' ' + app + ' skip ' + url)
            failed_app.append(app)
            continue

        app_ios = []
        for app_tag in apps_tag:
            # print(str(app.text).strip())
            value = str(app_tag.text).strip()
            value = value.encode().decode('unicode-escape')
            app_ios.append(value)

        similarities = [similar(org_app, i) for i in app_ios]
        index = similarities.index(max(similarities))
        #index = 0
        app_link = soup.find_all('div', {"class": "rf-serp-product-description"})[index].find('a', href=True)
        # print(app_link['href'])
        if app_link['href'] not in explored_links:
            explored_links.append(app_link['href'])
        else:
            print(app + 'explored ' + url)
            continue

        get_html2 = requests.get(app_link['href'])
        soup2 = BeautifulSoup(get_html2.text, 'html.parser')

        ratings = soup2.find('figcaption', {"class": "we-rating-count star-rating__count"})
        if ratings is None:
            ratings_tmp = [-1, -1, -1]
        else:
            ratings_tmp = ratings.text.split(' ')

        atr = {}

        score = ratings_tmp[0]
        number = ratings_tmp[2]
        atr['score'] = score
        atr['number'] = number

        descs = soup2.find_all('div', {"class": "information-list__item l-column small-12 medium-6 large-4 small-valign-top"})
        for desc in descs:
            dt = desc.find('dt').text.replace('\n', '').strip()
            dd = desc.find('dd').text.replace('\n', '').strip()
            atr[dt] = dd
            # print('dt: ' + dt + ' dd: ' + dd)

        ios_apps_metadata[app] = atr

    save_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/ios_apps_model_metadata_final.json'
    # print(failed_app)
    with open(save_path, 'w', encoding='utf8') as f:
        f.write(json.dumps(ios_apps_metadata, indent=4))

    failed_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/final_data/failed_ios_apps_model_metadata_final.txt'
    with open(failed_path, 'w', encoding='utf8') as f:
        for fa in failed_app:
            f.write(fa + '\n')


if __name__ == '__main__':
    #analysis()
    iosMetaDataCrawler_list()