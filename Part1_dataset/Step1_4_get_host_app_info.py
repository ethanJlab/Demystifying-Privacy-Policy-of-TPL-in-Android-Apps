# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux
import os
from Utils import check_macos_files

def main(host_apk_folder):
    apk_num = 0
    file_z = ""
    for TPL_cat in os.listdir(host_apk_folder):
        cat_folder = os.path.join(host_apk_folder, TPL_cat)
        if check_macos_files(TPL_cat) or os.path.isfile(cat_folder):
            continue
        for host_apk in os.listdir(cat_folder):
            if host_apk.startswith("."): continue
            if check_macos_files(host_apk): continue
            if host_apk.endswith('.apk') or host_apk.endswith('.xapk'):
                apk_num += 1
                continue
            else:
                apk_folder = os.path.join(cat_folder, host_apk)
                for apk in os.listdir(apk_folder):
                    if apk.startswith("."): continue
                    if apk.endswith('.apk') or apk.endswith('.xapk'):
                        apk_num += 1
    print('The number of distinct host apps in our dataset: %d' % (apk_num))

if __name__ == '__main__':
    host_apk_folder = '/ATPChecker/dataset/host_apk'
    main(host_apk_folder)
