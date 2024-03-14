# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/28
# System: linux
from Part2_PrivacyPolicyAnalysis.Constants import raw_SHARE_ACTION, raw_COLLECT_ACTION
from nltk import PorterStemmer

if __name__ == '__main__':
    processed_Sharing = []
    for i in raw_SHARE_ACTION:
        p = PorterStemmer().stem(i)
        print('%s ==> %s' % (i, p))
        processed_Sharing.append(p)
    processed_Collect = []
    for i in raw_COLLECT_ACTION:
        p = PorterStemmer().stem(i)
        print('%s ==> %s' % (i, p))
        processed_Collect.append(p)
    print("SHARE_ACTION=")
    print(list(set(processed_Sharing)))
    print("COLLECT_ACTION")
    print(list(set(processed_Collect)))

