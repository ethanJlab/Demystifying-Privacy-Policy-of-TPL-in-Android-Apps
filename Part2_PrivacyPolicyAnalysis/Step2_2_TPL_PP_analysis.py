# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux
from Part2_PrivacyPolicyAnalysis.PP_Analysis_Util import get_data_usage
from Utils import check_folder
import hanlp
import os


def main(tpl_pp_folder, save_root):
    check_folder(save_root)
    hanlp_mtl = hanlp.load(hanlp.pretrained.mtl.UD_ONTONOTES_TOK_POS_LEM_FEA_NER_SRL_DEP_SDP_CON_XLMR_BASE)
    for tpl_type in os.listdir(tpl_pp_folder):
        if '.DS_Store' in tpl_type: continue
        tpls_folder = os.path.join(tpl_pp_folder, tpl_type)
        for tpl_name in os.listdir(tpls_folder):
            tpl_pp_file = os.path.join(tpls_folder, tpl_name)
            save_name = os.path.join(save_root, tpl_name)
            print(tpl_pp_file)
            get_data_usage(tpl_pp_file, save_name, hanlp_mtl, print_flag=True)


if __name__ == '__main__':
    TPL_PP_preprocessed_folder = '../Results/preprocessed_pp/'
    TPL_PP_analysis_results = '../Results/TPL_pp_analysis_results'
    main(TPL_PP_preprocessed_folder, TPL_PP_analysis_results)
