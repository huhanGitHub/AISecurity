import json


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


#[3.7, 4.3, 4.4, 4.4, 4.8, 4.6, 4.7, 4.7, 4.8, 4.7, 4.7, 4.3, 4.7, 4.8, 4.7, 4.8, 4.5, 4.6, 4.7, 4.4, 4.8, 4.2, 4.9, 4.1, 4.2, 3.0, 3.2, 4.6, 4.5, 4.6, 3.6, 4.8, 4.6, 4.7, 3.2, 4.5, 3.9, 4.7, 4.5, 2.9, 4.8, 4.9, 4.3, 1.5, 4.3, 4.0, 4.2, 4.8, 4.6, 1.9, 4.0, 4.7, 4.8, 4.5, 4.4, 2.4, 4.5, 4.3, 4.8, 4.9, 2.9, 4.6, 4.8, 4.8, 4.3]
#[284.2, 214.3, 115.9, 475.0, 49.8, 54.1, 246.3, 453.7, 334.5, 299.4, 49.5, 115.7, 238.3, 243.9, 3800.0, 72.7, 191.7, 324.2, 272.5, 220.4, 170.5, 92.4, 127.1, 178.3, 212.7, 93.6, 110.9, 174.7, 218.1, 211.8, 166.5, 36.9, 174.8, 88.5, 137.4, 127.6, 115.4, 87.7, 324.6, 249.4, 288.4, 74.2, 170.2, 179.4, 188.8, 108.0, 184.7, 64.9, 285.8, 42.5, 50.1, 667.4, 161.2, 253.0, 174.6, 350.8, 79.7, 262.2, 70.1, 264.8, 788.1, 490.0, 55.4, 307.9, 109.6]
#1, 1, 1, 5.3, 62.4, 1, 69.8, 28.5, 651.3, 1000, 80.1, 1, 1000, 118.8, 2.9, 24.1, 1.4, 7.7, 17.0, 28.8, 8.0, 1, 419.9, 1, 11.9, 1, 1, 57.5, 1, 31.5, 1, 25.3, 113.9, 1.3, 1, 41.1, 1, 1.6, 447.2, 1, 1000, 1, 67.9, 1, 1.2, 4.9, 2.7, 1000, 580.5, 1, 1, 1.3, 1, 456.9, 28.2, 6.1, 632.1, 7.0, 4.5, 23.4, 5.7, 204.9, 40.2, 115.3, 1





if __name__ == '__main__':
    analysis()