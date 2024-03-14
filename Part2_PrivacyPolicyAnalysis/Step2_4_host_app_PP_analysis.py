# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/5/2
# System: linux
import os

from Part2_PrivacyPolicyAnalysis.PP_Analysis_Util import analyze_host_app_pp
from Utils import check_folder
import hanlp


def main(host_app_pp_preprocessed_folder, save_root):
    check_folder(save_root)
    hanlp_mtl = hanlp.load(hanlp.pretrained.mtl.UD_ONTONOTES_TOK_POS_LEM_FEA_NER_SRL_DEP_SDP_CON_XLMR_BASE)
    for tpl_category in os.listdir(host_app_pp_preprocessed_folder):
        if '.DS_Store' in tpl_category: continue
        pp_folder = os.path.join(host_app_pp_preprocessed_folder, tpl_category)
        for app_pp in os.listdir(pp_folder):
            if '.DS_Store' in app_pp: continue
            host_app_pp_file = os.path.join(pp_folder, app_pp)
            save_name = os.path.join(save_root, app_pp)
            print(host_app_pp_file)
            analyze_host_app_pp(host_app_pp_file, save_name, hanlp_mtl, print_flag=True)


if __name__ == '__main__':
    host_app_pp_preprocessed_folder = '../Results/preprocessed_hostapp_pp/'
    host_app_pp_analysis_results = '../Results/hostapp_pp_analysis_results'
    main(host_app_pp_preprocessed_folder, host_app_pp_analysis_results)
