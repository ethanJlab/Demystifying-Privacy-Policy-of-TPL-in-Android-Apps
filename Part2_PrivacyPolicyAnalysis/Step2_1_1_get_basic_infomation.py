# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux
import os
import re

from Part2_PrivacyPolicyAnalysis.Constants import SHARE_ACTION, COLLECT_ACTION, WWWWWH


def check_vague_data_collect(sentence):
    if "personal data" in sentence or "personal information" in sentence or "your data" in sentence or \
            "your information" in sentence or "user data" in sentence or "user information" in sentence:
        if "such as" in sentence or "for example" in sentence or ' not ' in sentence:
            return False
        return True
    return False


def preprocess_sen(sen):
    # remove unicode characters
    raw_sen = sen
    pattern = re.compile(r'[\uf001-\uf0ff]')
    sen = re.sub(pattern, '', sen).strip()
    tmp = sen.split(' ')
    if len(tmp) < 5:
        return sen, False
    return sen, True


def get_basic_information(tpl_folder, PRINT_FLAG):
    sentence_with_sacwords = []
    vag_sen = []
    vague_num = 0  # pi only
    sentence_num = 0
    num_wwwh = 0
    for z_type in os.listdir(tpl_folder):

        folder_2 = os.path.join(tpl_folder, z_type)
        if 'DS_Store' in z_type or not os.path.isdir(folder_2):
            continue
        for tpl_file in os.listdir(folder_2):
            sentence = []
            if 'DS_Store' in tpl_file or tpl_file.startswith('.'):
                continue
            file_name = os.path.join(folder_2, tpl_file)
            if PRINT_FLAG:
                print(file_name)
            f = open(file_name, 'r')
            # sentence = [i.split('\n')[0] for i in f.readlines()]

            context = f.readlines()

            for c in context:
                s = c.split('\n')
                #
                if len(s) > 2:
                    print("ERROR" + str(len(s)))
                    print(s)
                s = s[0]
                #
                sen = s.split('. ')
                sen = list(filter(None, sen))
                sentence.extend(sen)
            f.close()
            for sen in sentence:
                for i in WWWWWH:
                    if i in sen.lower():
                        num_wwwh += 1
                sen, c_flag = preprocess_sen(sen)
                if not c_flag:
                    continue
                for verb in SHARE_ACTION:
                    if ' ' + verb in sen.lower():
                        sentence_with_sacwords.append(verb + ":\t" + sen)
                        f = check_vague_data_collect(sen)
                        if f:
                            vague_num += 1
                            vag_sen.append(sen)
                        break
                if sen in vag_sen:
                    continue
                for verb in COLLECT_ACTION:
                    if ' ' + verb in sen.lower():
                        f = check_vague_data_collect(sen)
                        if f:
                            vague_num += 1
                            vag_sen.append(sen)
                        sentence_with_sacwords.append(verb + ":\t" + sen)
                        break
            sentence_num += len(sentence)

    if PRINT_FLAG:
        print("List of sentences wit sharing and collection words:")
        for s in sentence_with_sacwords:
            print('\t' + s)
        print("List of sentences ambiguously declaring data access behavior")
        for s in vag_sen:
            print('\t' + s)
    ret = ""
    ret += '============================================\n'
    ret += "Number of sentences in all privacy policies: %d\n" % (sentence_num)
    ret += "Number of sentences starting with 'who, why, when, whether, what, how': %d\n" % (num_wwwh)
    ret += "Number of sentences with sharing and collection (SAC) words: %d\n" % (len(sentence_with_sacwords))
    ret += "Number of sentences considered as SAC: %d\n" % (len(sentence_with_sacwords) - num_wwwh)
    ret += "Number of sentences ambiguously declaring data access behavior: %d\n" % (len(vag_sen))

    print(ret)
    return ret

