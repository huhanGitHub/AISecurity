import os


def batch_decompile(apk_dir, save_dir):
    for root, dirs, files in os.walk(apk_dir):
        for apk in files:
            if not str(apk).endswith('.apk'):
                continue
            apk_path = os.path.join(root, apk)
            app_save_dir = os.path.join(save_dir, apk)
            unit_decpmpile(apk_path, app_save_dir)


# /Users/hhuu0025/Downloads/SDK/build-tools/31.0.0/apksigner sign --ks /Users/hhuu0025/.android/debug.keystore /Users/hhuu0025/PycharmProjects/uiautomator2/activityMining/re_apks/bilibili_v1.16.2_apkpure.com.apk

#  /Users/hhuu0025/Downloads/SDK/build-tools/31.0.0/apksigner sign --ks activityMining/apkSignedKey --ks-key-alias key0 --ks-pass pass:123456 --key-pass pass:123456 --v4-signing-enabled false  /Users/hhuu0025/PycharmProjects/uiautomator2/activityMining/re_apks/youtube.apk

# /Users/hhuu0025/Downloads/SDK/build-tools/31.0.0/apksigner sign --ks /Users/hhuu0025/.android/debug.keystore --ks-pass pass:android --key-pass pass:android  /Users/h
# huu0025/PycharmProjects/uiautomator2/activityMining/re_apks/youtube.apk


def unit_decpmpile(apk_path, app_save_dir):
    print('Start apktool')
    cmd1 = 'apktool d ' + apk_path + ' -f -o ' + app_save_dir
    os.system(cmd1)


if __name__ == '__main__':

    apk_dir = r'/home/suyu/Documents/dataset/Suyu/data/tf_apks'
    save_dir = r'/home/suyu/Documents/dataset/Suyu/data//recompiled_tf_apks'

    batch_decompile(apk_dir, save_dir)


