# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux
import os

from Utils import check_macos_files


def main():
    statistics = {}
    TPL_without_pp = {}
    for TPL_cat in os.listdir(TPL_pp_folder):
        if TPL_cat.startswith("."):
            continue
        print(TPL_cat)
        cat_folder = os.path.join(TPL_pp_folder, TPL_cat)
        if check_macos_files(TPL_cat) or os.path.isfile(cat_folder):
            continue
        statistics[TPL_cat] = 0
        TPL_without_pp[TPL_cat] = []
        for TPL_name in os.listdir(cat_folder):
            if TPL_name.startswith("."):
                continue
            PP_FLAG = False
            pp_folder = os.path.join(cat_folder, TPL_name)
            if check_macos_files(pp_folder): continue
            for pp in os.listdir(pp_folder):
                if pp.endswith('.html'):
                    statistics[TPL_cat] += 1
                    print("\t" + TPL_name + ":\t" + pp)
                    PP_FLAG = True
                    break
            if not PP_FLAG:
                TPL_without_pp[TPL_cat].append(TPL_name)
    ###
    print(' ============================== ')
    print('List of TPLs without provide privacy policy before Apr-2022')
    for TPL_category in TPL_without_pp:
        print(TPL_category + ":")
        for TPL_name in TPL_without_pp[TPL_category]:
            print("\t" + TPL_name)
    ###
    print(' ============================== ')
    pp_num = 0
    for tpl_pp in statistics:
        print('\t%s: %d' % (tpl_pp, statistics[tpl_pp]))
        pp_num += statistics[tpl_pp]
    print('The dataset contains %d privacy policies' % (pp_num))


if __name__ == '__main__':
    TPL_pp_folder = "/ATPChecker/dataset/TPL_PP"
    main()
