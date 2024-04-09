import os
from Utils import check_macos_files

def count_host_apps(host_apk_folder):
    """
    Counts the number of distinct host apps (.apk or .xapk files) in a given dataset folder.
    
    :param host_apk_folder: The path to the folder containing host app categories and files.
    :return: The count of distinct host apps in the dataset.
    """
    apk_num = 0

    for TPL_cat in os.listdir(host_apk_folder):
        cat_folder = os.path.join(host_apk_folder, TPL_cat)
        if check_macos_files(TPL_cat) or os.path.isfile(cat_folder):
            continue
        for host_apk in os.listdir(cat_folder):
            if host_apk.startswith(".") or check_macos_files(host_apk):
                continue
            if host_apk.endswith('.apk') or host_apk.endswith('.xapk'):
                apk_num += 1
            else:
                apk_folder = os.path.join(cat_folder, host_apk)
                for apk in os.listdir(apk_folder):
                    if apk.startswith(".") or not (apk.endswith('.apk') or apk.endswith('.xapk')):
                        continue
                    apk_num += 1

    # Print the count for confirmation/debugging
    print(f'The number of distinct host apps in our dataset: {apk_num}')

    # Return the count
    return apk_num

# Example of how you would use it in another script:
# apk_count = count_host_apps("/path/to/host_apk_folder")
# print(f'Total distinct host apps: {apk_count}')
