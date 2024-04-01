import os

# Directory containing the scripts
script_dir_part1 = "/PART1_dataset"
script_dir_part2 = "/Part2_PrivacyPolicyAnalysis"
script_dir_part3 = "/Part3_BinaryFilesAnalysis"
script_dir_part4 = "/Part4_ResultsGenerator"

# Get all files in the directory
files1 = os.listdir(script_dir_part1)
files2 = os.listdir(script_dir_part2)
files3 = os.listdir(script_dir_part3)
files4 = os.listdir(script_dir_part4)

# Filter files that start with "Step1" and end with ".py"
scripts1 = [file for file in files1 if file.startswith("Step1") and file.endswith(".py")]

# Run each script
for script in scripts1:
    script_path = os.path.join(script_dir_part1, script)
    os.system(f"python {script_path}")