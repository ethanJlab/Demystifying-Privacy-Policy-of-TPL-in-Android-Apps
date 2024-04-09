# Assuming Utils.py is in the same directory or in your PYTHONPATH
from Utils import check_macos_files
import os


def tpl_statistics(TPL_list_folder):
    """
    Generates and prints statistics about TPL categories and counts in a given directory.

    :param TPL_list_folder: The path to the folder containing TPL categories and items.
    """
    statistics = {}
    for TPL_cat in os.listdir(TPL_list_folder):  # traverse categories of TPLs
        cat_folder = os.path.join(TPL_list_folder, TPL_cat)
        if check_macos_files(TPL_cat) or os.path.isfile(cat_folder):
            continue

        statistics[TPL_cat] = len([item for item in os.listdir(cat_folder) if not item.startswith(".")])

        print(TPL_cat)
        for TPL in os.listdir(cat_folder):
            if not TPL.startswith(".") and not check_macos_files(TPL):
                print('\t\"' + TPL + '\",')

    print(' ============================== ')
    TPL_List_num = sum(statistics.values())
    for cat, count in statistics.items():
        print(f'The number of TPLs in {cat}: {count}')

    print(f'\nTotal number of TPLs: {TPL_List_num}')
    print('Copyright of the list is reserved by AppBrain.')

# Example of how you would use it in another script
# import your_module_name_here
# your_module_name_here.tpl_statistics("../dataset/TPL_PP")
