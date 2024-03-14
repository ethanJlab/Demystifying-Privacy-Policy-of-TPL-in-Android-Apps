# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux

import os
from Utils import check_macos_files


def main(TPL_binaryfiles_folder):
    statistics = {}
    num_arr = 0
    num_jar = 0
    for TPL_cat in os.listdir(TPL_binaryfiles_folder):
        #
        cat_folder = os.path.join(TPL_binaryfiles_folder, TPL_cat)
        if check_macos_files(TPL_cat) or os.path.isfile(cat_folder):
            continue
        statistics[TPL_cat] = 0
        print(TPL_cat)
        for TPL in os.listdir(cat_folder):
            if check_macos_files(TPL) or TPL.startswith("."): continue
            binary_file_folder = os.path.join(cat_folder, TPL)
            for bf in os.listdir(binary_file_folder):
                if check_macos_files(bf): continue
                if bf.endswith('.jar'):
                    num_jar += 1
                    print("%s >> %s >> %s" % (TPL_cat, TPL, bf))
                    statistics[TPL_cat] += 1
                    break
                elif bf.endswith('.aar'):
                    num_arr += 1
                    print("%s >> %s >> %s" % (TPL_cat, TPL, bf))
                    statistics[TPL_cat] += 1
                    break
    #
    print(' ============================== ')
    print('The dataset contains %d distinct TPL binary files '
          'and includes %d *.jar files and %d *.aar files: ' % (num_jar + num_arr, num_jar, num_arr))
    #
    for tpl_cat in statistics:
        print('\t%s: %d' % (tpl_cat, statistics[tpl_cat]))

if __name__ == '__main__':
    TPL_binaryfiles_folder = '/ATPChecker/dataset/TPL_data'
    main(TPL_binaryfiles_folder)
