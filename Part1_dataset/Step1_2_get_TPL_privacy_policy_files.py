import os
from Utils import check_macos_files

def analyze_tpl_privacy_policies(TPL_pp_folder):
    """
    Analyzes TPL categories and counts the number of privacy policies present.
    
    :param TPL_pp_folder: The path to the folder containing TPL categories and items.
    :return: A tuple containing statistics and a list of TPLs without a privacy policy.
    """
    statistics = {}
    TPL_without_pp = {}

    for TPL_cat in os.listdir(TPL_pp_folder):
        if TPL_cat.startswith(".") or check_macos_files(TPL_cat):
            continue
        print(TPL_cat)
        cat_folder = os.path.join(TPL_pp_folder, TPL_cat)
        if os.path.isfile(cat_folder):
            continue
        statistics[TPL_cat] = 0
        TPL_without_pp[TPL_cat] = []

        for TPL_name in os.listdir(cat_folder):
            if TPL_name.startswith("."):
                continue
            PP_FLAG = False
            pp_folder = os.path.join(cat_folder, TPL_name)
            if check_macos_files(pp_folder): 
                continue
            for pp in os.listdir(pp_folder):
                if pp.endswith('.html'):
                    statistics[TPL_cat] += 1
                    print("\t" + TPL_name + ":\t" + pp)
                    PP_FLAG = True
                    break
            if not PP_FLAG:
                TPL_without_pp[TPL_cat].append(TPL_name)

    # Printing and returning the statistics
    print(' ============================== ')
    print('List of TPLs without provide privacy policy before Apr-2022')
    for TPL_category, TPL_names in TPL_without_pp.items():
        print(TPL_category + ":")
        for TPL_name in TPL_names:
            print("\t" + TPL_name)

    print(' ============================== ')
    pp_num = sum(statistics.values())
    for tpl_cat, num_pp in statistics.items():
        print(f'\t{tpl_cat}: {num_pp}')
    print(f'The dataset contains {pp_num} privacy policies')

    return statistics, TPL_without_pp

# Example of how you would use it in another script:
# stats, tpl_without_pp = analyze_tpl_privacy_policies("/path/to/TPL_PP")
# print(stats)
# print(tpl_without_pp)
