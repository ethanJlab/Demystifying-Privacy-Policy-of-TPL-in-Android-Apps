# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/5/2
# System: linux
import os

from Part2_PrivacyPolicyAnalysis.html_process_util import processFile
from Utils import check_folder


def main(host_app_pp_folder, save_folder):
    check_folder(save_folder)
    for tpl_category in os.listdir(host_app_pp_folder):
        path_1 = os.path.join(host_app_pp_folder, tpl_category)
        if 'DS_Store' in path_1: continue
        save_folder_1 = os.path.join(save_folder, tpl_category)
        check_folder(save_folder_1)
        for app_name in os.listdir(path_1):
            if 'DS_Store' in app_name: continue
            path_2 = os.path.join(path_1, app_name)
            for html_file in os.listdir(path_2):
                if html_file.endswith('html'):
                    pp_file = os.path.join(path_2, html_file)
                    processFile(pp_file, save_folder_1)
                    break


if __name__ == '__main__':
    host_app_pp_folder = '/dataset/host_app_pp'
    pp_save_folder = '../Results/preprocessed_hostapp_pp/'
    main(host_app_pp_folder, pp_save_folder)
