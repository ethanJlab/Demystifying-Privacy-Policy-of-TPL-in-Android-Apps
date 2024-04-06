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

# Define the path to the TPL list folder you want to analyze
tpl_list_folder_path = "dataset/TPL_PP"
tpl_data_folder_path = "dataset/TPL_data"
host_apk_folder_path = "dataset/host_apk"

# Part 2 output locations
preprocessed_pp_save_folder = '../Results/preprocessed_pp/'


# Part 2 outputs
#get_basic_information(preprocessed_pp_save_folder, False)

# Part 2 Jobs
#analyze_pp(tpl_list_folder_path, preprocessed_pp_save_folder)
preprocess_hostapp_pp(host_apk_folder_path, preprocessed_pp_save_folder)
#analyze_hostapp_pp(preprocessed_pp_save_folder)
#analyze_256app_pp(preprocessed_pp_save_folder)



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

print("\nReturned analyze_tpl_privacy_policies_output:")
print(analyze_tpl_privacy_policies_output)

print("\nReturned analyze_tpl_binaryfiles_output:")
print(analyze_tpl_binaryfiles_output)

print("\nReturned host_apps_count:")
print(host_apps_count)

# Print outputs for Part 2
print("\n Completed pre-process_privacy_policies")



