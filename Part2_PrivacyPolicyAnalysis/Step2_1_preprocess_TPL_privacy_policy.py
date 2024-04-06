# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux
import os
from Part2_PrivacyPolicyAnalysis.html_process_util import processFile
from Utils import check_folder


def preprocess_privacy_policies(tpl_pp_folder, save_folder):
    ## TPL pp

    check_folder(save_folder)
    for tpl_type in os.listdir(tpl_pp_folder):
        path_1 = os.path.join(tpl_pp_folder, tpl_type)
        if (not os.path.isdir(path_1)) or 'DS_Store' in path_1:
            continue
        save_folder_2 = os.path.join(save_folder, tpl_type)
        check_folder(save_folder_2)
        for tpl_name in os.listdir(path_1):
            path_2 = os.path.join(path_1, tpl_name)
            if (not os.path.isdir(path_2)) or 'DS_Store' in path_2:
                continue
            for html_file in os.listdir(path_2):
                if not html_file.endswith('html'):
                    continue
                pp_file = os.path.join(path_2, html_file)
                # save_file = os.path.join(save_folder_2, tpl_type + '_' + tpl_name + '.txt')
                processFile(pp_file, save_folder_2)
                print(html_file + " Has been processed")
        # When finished
        print("Processing Completed")

