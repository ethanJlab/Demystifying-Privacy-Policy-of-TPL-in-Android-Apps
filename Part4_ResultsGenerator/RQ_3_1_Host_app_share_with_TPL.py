# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/5/7
# System: linux

import os

from Utils import check_macos_files


def main(rp, hap):
    share_count = 0
    apk_list = []
    for TPL_cat in os.listdir(hap):
        cat_folder = os.path.join(hap, TPL_cat)
        if check_macos_files(TPL_cat) or os.path.isfile(cat_folder):
            continue
        for host_apk in os.listdir(cat_folder):
            if check_macos_files(host_apk) or host_apk.startswith('.'): continue
            if host_apk.endswith('.apk'):  # or host_apk.endswith('.xapk'):
                if os.path.getsize(os.path.join(cat_folder, host_apk)) / (1024 * 1024) > 100:
                    continue
                apk_list.append(host_apk + '.txt')
                continue
            else:
                apk_folder = os.path.join(cat_folder, host_apk)
                for apk in os.listdir(apk_folder):
                    if apk.endswith('.apk'):  # or apk.endswith('.xapk'):
                        if os.path.getsize(os.path.join(apk_folder, apk)) / (1024 * 1024) > 100:
                            continue
                        apk_list.append(host_apk + '.txt')
    for i in os.listdir(rp):
        target_file = os.path.join(rp, i)
        if i in apk_list:
            f = open(target_file, 'r')
            context = f.readlines()
            for j in context:
                if j.startswith('\tPI'):
                    share_count += 1

                    break
    app_num = len(os.listdir(results_path)) - 1  # minus the DS_Store
    print("%d /%d (%f %%) Host apps share data with TPLs" % (share_count, app_num, share_count / app_num))


if __name__ == '__main__':
    results_path = '/Results/host_app_binary_results'
    host_app_path = '/ATPChecker/dataset/host_apk'
    main(results_path, host_app_path)
