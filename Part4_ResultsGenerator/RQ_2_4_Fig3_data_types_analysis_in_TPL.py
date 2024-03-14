# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/5/10
# System: linux

import os
from matplotlib import pyplot as plt

data_map = {
    "get_account": "account",
    "email": "email",
    "contact": "contact",
    "advertisingidClient getadvertisingidInfo": "adid",
    "advertisingidClient getInfo": "adid",
    "android.bluetooth.BluetoothAdapter getAddress": "bluetooth",
    "android.hardware.Camera setPreviewDisplay": "camera",
    "android.telephony.TelephonyManager getCellLocation": "location",
    "android.provider.ContactsContract PhoneLookup": "contact",
    "android.location.Location getLatitude": "location",
    "android.location.Location getLongitude": "location",
    "android.location.LocationManager getLastKnownLocation": "location",
    "android.location.LocationManager requestLocationUpdates": "location",
    "android.location.LocationManager getLongitude": "location",
    "android.telephony.TElephonyManager getSimSerialNumber": "sim",
    "android.telephony.TElephonyManager getDeviceId": "deviceid",
    "android.telephony.TElephonyManager getSubscriberId": "imse",
    "java.util.Calendar getTimeZone": "location",
    "android.net.wifi.WifiInfo getMacAddress": "mac",
    "macaddress": "mac",
    "android.media.MediaRecorder getAudioSource": "media",
    "android.media.MediaRecorder startRecording": "media",
    "android.accounts.AccountManager getPassword": "password",
    "android.telephony.TelephonyManager getLine1Number": "phonenumber",
    "phonenumber": "phonenumber",
    "android.hardware.SensorManager getDefaultSensor": "sensor",
    "android.telephony.SmsManager sendTextMessage": "sms",
    "android.net.wifi.WifiInfo getSSID": "ssid",
    "android.accounts.AccountManager getAccounts": "account",
    "android.os.UserManager getUserName": "username",
    "username": "username",
    "getadvertisingidInfo": "adid",
}

keyword_list = ["email",
                "password",
                "network"]


def inter(a, b):
    return list(set(a.split(' ')) & set(b.split(' ')))


TARGET_DATA = ["phonenumber",
               "adid", "advertising id", "bluetooth", "contact",
               "email",
               "imei",
               "deviceid",
               "network",
               " sim", " sms", "location", "address", " imse",
               "mac address", "mac",
               "phone number", "ssid", "user credential",
               "username",
               "password", "account",
               "wifi address", "wifi",
               "macaddress",
               "googleadvertiserid",
               "idvertisinginfo",
               "photos"]


def get_TPL_data_flow_statistics(target_folder):
    statistics = {}
    trace = {}
    tpl_access_user_data = {}
    for rf in os.listdir(target_folder):
        if 'DS_Store' in rf or rf == '\n':
            continue
        file_name = os.path.join(target_folder, rf)
        f = open(file_name, 'r')
        data = f.readlines()
        f.close()
        TPL_data = {}
        for i, line in enumerate(data):
            if line.startswith('stmt:'):
                tmp = data[i + 1]
                data_api = tmp.split('\t')[2].replace('\n', '')
                data_type = data_map[data_api]
                if data_type not in statistics:
                    statistics[data_type] = []
                statistics[data_type].append(line.replace('stmt:\t', '').replace('\n', ''))
                # print(data_api + '\t' + line)
                #
                tpl_name = rf.replace('.txt', '')
                if tpl_name not in tpl_access_user_data:
                    tpl_access_user_data[tpl_name] = {}
                if data_type not in tpl_access_user_data[tpl_name]:
                    tpl_access_user_data[tpl_name][data_type] = []
                tpl_access_user_data[tpl_name][data_type].append(line)
                #
                if line not in trace:
                    trace[line] = 0
                trace[line] += 1
    for i in statistics:
        statistics[i] = list(set(statistics[i]))
    #
    tpl_access_user_data_list = list(set(tpl_access_user_data))
    #
    trace_num = 0
    for i in trace:
        trace_num += trace[i]
    #
    data_statistic = {}
    for i in statistics:
        data_statistic[i] = len(statistics[i])
    tmp = sorted(data_statistic.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    ##
    tpl_data_results = {}

    ###
    f = open("TPL_data_for_manual_check.csv", "w")
    for tpl_name in tpl_access_user_data:
        for data_type in tpl_access_user_data[tpl_name]:
            if data_type not in tpl_data_results:
                tpl_data_results[data_type] = 0
            tpltmp = list(set(tpl_access_user_data[tpl_name][data_type]))
            ###
            for lline in tpltmp:
                c = lline.replace('stmt:\t', '').replace('\n', '')
                f.write("%s,%s,%s\n" % (tpl_name, data_type, c))
            ###
            tpl_data_results[data_type] += len(tpltmp)
    tpl_data_results = dict(sorted(tpl_data_results.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    return tpl_data_results


def get_TPL_pp_data_statistics(results_folder):
    data_type_count = {}
    data_type_sent = {}
    for tpl_type in os.listdir(results_folder):
        if "DS_Store" in tpl_type:
            continue
        folder_2 = os.path.join(results_folder, tpl_type)
        file_name = folder_2
        f = open(file_name, 'r')
        data = f.readlines()
        for tmp in data:
            if not tmp.startswith('\t'):
                continue
            tmp = tmp.lower()
            for i in TARGET_DATA:
                if i in tmp:
                    if not i in data_type_count:
                        data_type_count[i] = 1
                        data_type_sent[i] = []
                    else:
                        data_type_count[i] += 1
                        data_type_sent[i].append(tmp)
    tpl_pp_results = dict(sorted(data_type_count.items(), key=lambda item: item[1], reverse=True))
    return tpl_pp_results


def draw_fig3(TPL_data_flow_results_folder, TPL_pp_results_folder):
    tpl_pp_results = get_TPL_pp_data_statistics(TPL_pp_results_folder)
    tpl_df_results = get_TPL_data_flow_statistics(TPL_data_flow_results_folder)
    pp_label = [i for i in tpl_pp_results][0:11]
    data_label = [i for i in tpl_df_results][0:11]
    TPL_PP = [tpl_pp_results[i] for i in tpl_pp_results][0:11]
    TPL_data_flow = [tpl_df_results[i] for i in tpl_df_results][0:11]
    print("TPL PP data statistics:")
    for i in tpl_pp_results:
        print("%s:%d" % (i, tpl_pp_results[i]))
    print("TPL data flow statistics:")
    for i in tpl_df_results:
        print("%s:%d" % (i, tpl_df_results[i]))

    for i, d in enumerate(data_label):
        if d == "password":
            data_label[i] = "pw"
        if d == "location":
            data_label[i] = "loc"
        if d == "phonenumber":
            data_label[i] = "phnum"

    # preprocess data for better illustration
    TPL_PP_show = [i / 10 for i in TPL_PP]
    TPL_data_flow_show = [-i for i in TPL_data_flow]
    #
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    #
    # plot bar to show statistics of the times of data usage in TPL privacy policies and TPL dataflow
    plt.bar(index, TPL_PP_show, label='data usage in TPL PP', color=['coral'])
    plt.bar(index, TPL_data_flow_show, label='data usage in TPL data flow', color=['dodgerblue'])
    #
    text_x = [i for i in range(1, 12)]
    pp_y = [i + 2 for i in TPL_PP_show]
    #
    text_kwargs = dict(ha='center', va='bottom', fontsize=12)
    for i in range(len(text_x)):
        plt.text(text_x[i], pp_y[i], pp_label[i], **text_kwargs, rotation=45)
    #
    tpl_y = [i - 7 for i in TPL_data_flow_show]
    for i in range(len(text_x)):
        plt.text(text_x[i], tpl_y[i], data_label[i], **text_kwargs, rotation=45)
    #
    y_label = [i for i in range(-100, 70, 20)]
    # y_label = [-100, -80, -60, -40, -20, 0, ]
    y_ticks = ['100', '80', '60', '40', '20', '0', '200', '400','600']

    ticks_kwargs = dict(fontsize=12, fontname='Courier', fontweight='bold')
    plt.yticks(y_label, y_ticks, **ticks_kwargs)
    #
    plt.grid(axis='y')
    #
    bwith = 2.5
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)
    #
    plt.legend()
    plt.savefig('./Fig3.pdf')
    plt.show()


if __name__ == '__main__':
    TPL_data_flow_results_folder = "../Results/TPL_binary_results"
    TPL_pp_results_folder = "../Results/TPL_pp_analysis_results"
    draw_fig3(TPL_data_flow_results_folder, TPL_pp_results_folder)
