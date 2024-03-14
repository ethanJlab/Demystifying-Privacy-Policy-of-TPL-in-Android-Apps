# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux
import os


def check_macos_files(f: str):
    if '.DS_Store' in f:
        return True
    else:
        return False


def check_folder(foler_path: str):
    if not os.path.exists(foler_path):
        os.makedirs(foler_path)
