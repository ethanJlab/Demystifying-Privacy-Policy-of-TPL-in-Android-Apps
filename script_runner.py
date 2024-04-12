# Part 1 imports
from Part1_dataset.Step1_1_get_TPL_list_info import tpl_statistics
from Part1_dataset.Step1_2_get_TPL_privacy_policy_files import analyze_tpl_privacy_policies
from Part1_dataset.Step1_3_get_TPL_binaryfiles_info import analyze_tpl_binary_files
from Part1_dataset.Step1_4_get_host_app_info import count_host_apps

# Part 2 imports
from Part2_PrivacyPolicyAnalysis.Step2_1_preprocess_TPL_privacy_policy import preprocess_privacy_policies
from Part2_PrivacyPolicyAnalysis.Step2_1_1_get_basic_infomation import get_basic_information
from Part2_PrivacyPolicyAnalysis.Step2_2_TPL_PP_analysis import analyze_pp
from Part2_PrivacyPolicyAnalysis.Step2_3_preprocess_hostapp_pp import preprocess_hostapp_pp
from Part2_PrivacyPolicyAnalysis.Step2_4_host_app_PP_analysis import analyze_hostapp_pp
from Part2_PrivacyPolicyAnalysis.Step3_256app_privacy_policy_analysis import analyze_256app_pp

# Part 3 is ran seperate

# Part 4 imports
from Part4_ResultsGenerator.RQ_2_1_TPL_dataflow_results import get_data_flow_results
from Part4_ResultsGenerator.RQ_2_2_TPL_compliance_analysis import TPL_compliance_analysis
from Part4_ResultsGenerator.RQ_2_3_Fig2_FCG_evaluation import generate_FCG_evaluation
from Part4_ResultsGenerator.RQ_2_4_Fig3_data_types_analysis_in_TPL import data_flow_analysis_in_TPL
from Part4_ResultsGenerator.RQ_3_1_Host_app_share_with_TPL import Host_app_share_with_TPL
from Part4_ResultsGenerator.RQ_3_2_Draw_fig_5 import draw_fig_5
from Part4_ResultsGenerator.RQ_4_Identify_app_conpliance import get_apk_name_map



TESTP1 = True
TESTP4 = False

# Define the path to the TPL list folder you want to analyze
tpl_list_folder_path = "dataset/TPL_PP"
tpl_data_folder_path = "dataset/TPL_data"
host_apk_folder_path = "dataset/host_apk"

prelude_list = []
p1_list = []
p2_list = []
p3_list = []
p4_list = []


# Part 2 output locations
preprocessed_pp_save_folder = 'Results/preprocessed_pp/'
temp_save = 'Save/'

if TESTP1:
    # Part 2 outputs
    prelude_list.append(get_basic_information(preprocessed_pp_save_folder, False))

    # Part 2 Jobs
    #analyze_pp(tpl_list_folder_path, preprocessed_pp_save_folder)
    prelude_list.append(preprocess_hostapp_pp(host_apk_folder_path, preprocessed_pp_save_folder))
    #analyze_hostapp_pp(preprocessed_pp_save_folder)
    #analyze_256app_pp(preprocessed_pp_save_folder,temp_save)



    # Part 1 outputs
    tpl_statistics_output = tpl_statistics(tpl_list_folder_path)
    analyze_tpl_privacy_policies_output = analyze_tpl_privacy_policies(tpl_list_folder_path)
    analyze_tpl_binaryfiles_output = analyze_tpl_binary_files(tpl_data_folder_path)
    host_apps_count = count_host_apps(host_apk_folder_path)

    # Part 2 outputs
    preprocess_privacy_policies(tpl_list_folder_path, preprocessed_pp_save_folder)

    # Print outputs for Part 1
    print("Returned tpl_statistics_output:")
    print(tpl_statistics_output)
    p1_list.append("Returned tpl_statistics_output:")
    p1_list.append(tpl_statistics_output)

    print("\nReturned analyze_tpl_privacy_policies_output:")
    print(analyze_tpl_privacy_policies_output)
    p1_list.append("\nReturned analyze_tpl_privacy_policies_output:")
    p1_list.append(analyze_tpl_privacy_policies_output)

    print("\nReturned analyze_tpl_binaryfiles_output:")
    print(analyze_tpl_binaryfiles_output)
    p1_list.append("\nReturned analyze_tpl_binaryfiles_output:")
    p1_list.append(analyze_tpl_binaryfiles_output)

    print("\nReturned host_apps_count:")
    print(host_apps_count)
    p1_list.append("\nReturned host_apps_count:")
    p1_list.append(host_apps_count)

    # Print outputs for Part 2
    print("\n Completed pre-process_privacy_policies")
    p2_list.append("\n Completed pre-process_privacy_policies")


# Part 4 outputs
if TESTP4:
    TEST_PART = True
    if not TEST_PART:
        print("\n Running get_data_flow_results")
        p4_list.append("\n Running get_data_flow_results")
        data_flow = get_data_flow_results("Results/TPL_binary_results")
        for item in data_flow:
            p4_list.append(item)
            # p4_list.append("end of item")
        print("\n Completed get_data_flow_results")
        p4_list.append("\n Completed get_data_flow_results")

    if not TEST_PART:
        print("\n Running TPL_compliance_analysis")
        TPL_compliance_analysis_output = TPL_compliance_analysis()
        print("\n Completed TPL_compliance_analysis")
        print(TPL_compliance_analysis_output)
        p4_list.append("\n Running TPL_compliance_analysis")
        p4_list.append(TPL_compliance_analysis_output)
        p4_list.append("\n Completed TPL_compliance_analysis")

    if TEST_PART:
        print("\n Running generate_FCG_evaluation")
        generate_FCG_evaluation_output = generate_FCG_evaluation()
        print("\n Completed generate_FCG_evaluation")
        print(generate_FCG_evaluation_output)
        p4_list.append("\n Running generate_FCG_evaluation")
        p4_list.append(generate_FCG_evaluation_output)
        p4_list.append("\n Completed generate_FCG_evaluation")

    # print("\n Running data_flow_analysis_in_TPL")
    # data_flow_analysis_in_TPL_output = data_flow_analysis_in_TPL("Results/TPL_binary_results", "Results/TPL_pp_analysis_results")
    # print("\n Completed data_flow_analysis_in_TPL")
    # print(data_flow_analysis_in_TPL_output)

    if not TEST_PART:
        print("\n Running Host_app_share_with_TPL")
        Host_app_share_with_TPL_output = Host_app_share_with_TPL("Results/host_app_binary_results", host_apk_folder_path)
        print("\n Completed Host_app_share_with_TPL")
        print(Host_app_share_with_TPL_output)
        p4_list.append("\n Running Host_app_share_with_TPL")
        p4_list.append(Host_app_share_with_TPL_output)
        p4_list.append("\n Completed Host_app_share_with_TPL")

        print("\n Running draw_fig_5")
        draw_fig_5_output = draw_fig_5("Results/host_app_binary_results")
        print("\n Completed draw_fig_5")
        print("Fig 5 location: "+ draw_fig_5_output)
        p4_list.append("\n Running draw_fig_5")
        # here is a png
        p4_list.append(draw_fig_5_output)
        p4_list.append("\n Completed draw_fig_5")


print("\n Running get_apk_name_map")
#get_apk_name_map_output = get_apk_name_map()
print("\n Completed get_apk_name_map")
#print(get_apk_name_map_output)
print("End of Script runner")


# For PDF script connection: List implementation and PDF function use will go here




