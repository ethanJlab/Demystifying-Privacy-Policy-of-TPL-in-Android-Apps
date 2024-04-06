# Example script to use the tpl_statistics function from the tpl_analyzer module

# First, import the tpl_statistics function from the tpl_analyzer module
from Part1_dataset.Step1_1_get_TPL_list_info import tpl_statistics

# Define the path to the TPL list folder you want to analyze
tpl_list_folder_path = "dataset/TPL_PP"

# Call the tpl_statistics function with the path to your TPL list folder
# The function will print the statistics and also return them as a string
statistics_output = tpl_statistics(tpl_list_folder_path)

# If you wish to use the returned statistics output for further processing or logging,
# you can do so here. For demonstration, we'll just print the returned value again.
print("Returned Statistics Output:")
print(statistics_output)
