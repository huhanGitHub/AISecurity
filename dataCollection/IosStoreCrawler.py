from bs4 import BeautifulSoup
import requests
import json
from modelComparator.compareModelNames import similar
from urllib.request import urlopen, Request


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


def convertJson2text():
    json_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/android_apps_with_models.json'
    apps = json.load(open(json_path, 'r', encoding='utf8'))
    keys = apps.keys()

    keys = [i.replace('\n', '').strip() for i in keys]

    currents_apps_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/pkgs.txt'
    all_apps = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/all_apps.txt'
    currents_apps = open(currents_apps_path, 'r', encoding='utf8').readlines()
    currents_apps = [i.replace('\n', '').strip() for i in currents_apps]

    valid_apps = open(r'/Users/hhuu0025/PycharmProjects/AISecurity/data/valid_apps.txt', 'r', encoding='utf8').readlines()
    valid_apps = [i.replace('\n', '').strip() for i in valid_apps]

    for key in keys:
        if key not in currents_apps:
            currents_apps.append(key)

    for valid_app in valid_apps:
        if valid_app not in currents_apps:
            currents_apps.append(valid_app)

    with open(all_apps, 'w', encoding='utf8') as f:
        for line in currents_apps:
            f.write(line + '\n')





def topFreeAppCrawler():
    app_store_cate = ['Books', 'Business', 'Developer Tools', 'Education', 'Entertainment', 'Finance', 'Food & Drink',
                      'Graphic & Design', 'Health & Fitness', 'Kids', 'Lifestyle', 'Magazines & Newspapers', 'Medical',
                      'Music', 'Navigation', 'News', 'Photo & Video', 'Productivity', 'Reference', 'Shopping',
                      'Social Networking', 'Sports', 'Travel', 'Utilities', 'Weather']

    app_store_cate_links = ['https://apps.apple.com/us/charts/iphone/books-apps/6018', 'https://apps.apple.com/us/charts/iphone/business-apps/6000',
                            'https://apps.apple.com/us/charts/iphone/developer-tools-apps/6026', 'https://apps.apple.com/us/charts/iphone/education-apps/6017',
                            'https://apps.apple.com/us/charts/iphone/entertainment-apps/6016', 'https://apps.apple.com/us/charts/iphone/finance-apps/6015',
                            'https://apps.apple.com/us/charts/iphone/food-drink-apps/6023', 'https://apps.apple.com/us/charts/iphone/graphics-design-apps/6027',
                            'https://apps.apple.com/us/charts/iphone/health-fitness-apps/6013', 'https://apps.apple.com/us/charts/iphone/kids-apps/36?ageId=0',
                            'https://apps.apple.com/us/charts/iphone/lifestyle-apps/6012', 'https://apps.apple.com/us/charts/iphone/magazines-newspapers-apps/6021',
                            'https://apps.apple.com/us/charts/iphone/medical-apps/6020', 'https://apps.apple.com/us/charts/iphone/music-apps/6011',
                            'https://apps.apple.com/us/charts/iphone/navigation-apps/6010', 'https://apps.apple.com/us/charts/iphone/news-apps/6009',
                            'https://apps.apple.com/us/charts/iphone/photo-video-apps/6008', 'https://apps.apple.com/us/charts/iphone/productivity-apps/6007',
                            'https://apps.apple.com/us/charts/iphone/reference-apps/6006', 'https://apps.apple.com/us/charts/iphone/shopping-apps/6024',
                            'https://apps.apple.com/us/charts/iphone/social-networking-apps/6005', 'https://apps.apple.com/us/charts/iphone/sports-apps/6004',
                            'https://apps.apple.com/us/charts/iphone/travel-apps/6003', 'https://apps.apple.com/us/charts/iphone/utilities-apps/6002',
                            'https://apps.apple.com/us/charts/iphone/weather-apps/6001']

    top_free_field = r'?chart=top-free'
    top_apps = []
    failed_urls = []
    save_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/topAppleApps/topAppleApps.txt'
    for link in app_store_cate_links:
        top_cate_apps = []
        url = link + top_free_field
        status_code = 0
        get_html = ''
        while status_code != 200:
            get_html = requests.get(url)
            # print(get_html.text)
            status_code = get_html.status_code
            if status_code != 200:
                print('fail, request again ' + url)

        soup = BeautifulSoup(get_html.text, 'lxml')

        apps = soup.find_all('div', class_='we-lockup__title')
        for app in apps:
            cls = app.attrs.get('class', 0)
            if cls != 0:
                text = app.text.replace('\n', '').strip()
                #print(text + '---' + str(cls))
                print(text)
                top_cate_apps.append(text)

        top_apps.append(top_cate_apps)

    with open(save_path, 'w', encoding='utf8') as f:
        for i in range(len(top_apps)):
            f.write('category: ' + app_store_cate[i] + '\n')
            for app in top_apps[i]:
                f.write(app + '\n')


# ['we-lockup__text']
# <div class="we-clamp we-clamp--visual" data-clamp="" style="--clamp-lines: 2" dir="ltr">Instagram</div>



if __name__ == '__main__':
    targets = ['wechat', 'image', 'xxxxxx']
    save_path = r'../data/android_ios_app_pairs_all.json'

    # app_list_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/valid_apps.txt'
    app_list_path = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/all_apps.txt'
    #app_list = read_app_list(app_list_path)

    # batch_crawler_app_store(app_list, save_path)
    iosMetaDataCrawler_list()

    #topFreeAppCrawler()