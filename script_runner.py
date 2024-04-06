# Part 1 imports
from Part1_dataset.Step1_1_get_TPL_list_info import tpl_statistics
from Part1_dataset.Step1_2_get_TPL_privacy_policy_files import analyze_tpl_privacy_policies
from Part1_dataset.Step1_3_get_TPL_binaryfiles_info import analyze_tpl_binary_files
from Part1_dataset.Step1_4_get_host_app_info import count_host_apps

# Define the path to the TPL list folder you want to analyze
tpl_list_folder_path = "dataset/TPL_PP"
tpl_data_folder_path = "dataset/TPL_data"
host_apk_folder_path = "dataset/host_apk"

# Call the tpl_statistics function with the path to your TPL list folder
# The function will print the statistics and also return them as a string
tpl_statistics_output = tpl_statistics(tpl_list_folder_path)
analyze_tpl_privacy_policies_output = analyze_tpl_privacy_policies(tpl_list_folder_path)
analyze_tpl_binaryfiles_output = analyze_tpl_binary_files(tpl_data_folder_path)
host_apps_count = count_host_apps(host_apk_folder_path)

# Print outputs for Part 1
print("Returned tpl_statistics_output:")
print(tpl_statistics_output)

print("\nReturned analyze_tpl_privacy_policies_output:")
print(analyze_tpl_privacy_policies_output)

print("\nReturned analyze_tpl_binaryfiles_output:")
print(analyze_tpl_binaryfiles_output)

print("\nReturned host_apps_count:")
print(host_apps_count)

