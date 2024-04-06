import os
from Utils import check_macos_files

def analyze_tpl_binary_files(TPL_binaryfiles_folder):
    """
    Analyzes TPL binary files, counting distinct TPL binary files, jar, and aar files.
    
    :param TPL_binaryfiles_folder: The path to the folder containing TPL binary files.
    :return: A dictionary with statistics on the TPL binary files, and counts of jar and aar files.
    """
    statistics = {}
    num_jar = 0
    num_aar = 0

    for TPL_cat in os.listdir(TPL_binaryfiles_folder):
        cat_folder = os.path.join(TPL_binaryfiles_folder, TPL_cat)
        if check_macos_files(TPL_cat) or os.path.isfile(cat_folder):
            continue

        statistics[TPL_cat] = 0
        print(TPL_cat)

        for TPL in os.listdir(cat_folder):
            if check_macos_files(TPL) or TPL.startswith("."):
                continue

            binary_file_folder = os.path.join(cat_folder, TPL)
            for bf in os.listdir(binary_file_folder):
                if check_macos_files(bf):
                    continue
                if bf.endswith('.jar'):
                    num_jar += 1
                    statistics[TPL_cat] += 1
                elif bf.endswith('.aar'):
                    num_aar += 1
                    statistics[TPL_cat] += 1
                if bf.endswith('.jar') or bf.endswith('.aar'):
                    print("%s >> %s >> %s" % (TPL_cat, TPL, bf))
                    break

    summary = {
        'statistics': statistics,
        'total_binary_files': num_jar + num_aar,
        'num_jar': num_jar,
        'num_aar': num_aar,
    }

    print(' ============================== ')
    print(f'The dataset contains {summary["total_binary_files"]} distinct TPL binary files '
          f'and includes {summary["num_jar"]} *.jar files and {summary["num_aar"]} *.aar files.')

    for tpl_cat, count in statistics.items():
        print(f'\t{tpl_cat}: {count}')

    return summary

# Example of how you would use it in another script:
# summary = analyze_tpl_binary_files("/path/to/TPL_binaryfiles_folder")
# print(summary)
