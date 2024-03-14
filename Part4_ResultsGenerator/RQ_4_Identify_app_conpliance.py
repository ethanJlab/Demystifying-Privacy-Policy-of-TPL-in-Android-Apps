# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/8/16
# System: linux
import os
import re

from Util_Table5 import get_tpl_pack_name_map

TPL_map = {
    'alipay': 'alipay',
    'com.baidu': 'baidu',
    'umeng': 'youmeng',
    'com.tencent': 'tencent',
    'androidx.appcompat': 'androidx.appcompat',
    'org.json': 'org.json',
    'com.google.android.gms': 'com.google.android.gms',
    'androidx.activity': 'androidx.activity'
}

API2DataMap = {
    "email": "email",
    "password": "password",
    "network": "network",
    "advertisingidClient getadvertisingidInfo": "adid",
    "advertisingidClient getadInfo": "adid",
    "android.bluetooth.BluetoothAdapter getAddress": "bluetooth",
    "android.telephony.TelephonyManager getCellLocation": "location",
    "android.telephony.TelephonyManager getCellLocation ": "location",

    "android.provider.ContactsContract PhoneLookup": "contact",
    "android.location.Location getLatitude": "location",
    "android.location.Location getLatitude ": "location",

    "android.location.Location getLongitude": "location",
    "android.location.Location getLongitude ": "location",

    "android.location.LocationManager getLastKnownLocation": "location",
    "android.location.LocationManager requestLocationUpdates": "location",
    "android.location.LocationManager getLongitude": "location",
    "android.telephony.TelephonyManager getSimSerialNumber": "sim",
    "android.telephony.TelephonyManager getDeviceId": "device id",
    "android.telephony.TelephonyManager getDeviceId ": "device id",
    "android.telephony.TelephonyManager getSubscriberId": "imse",
    "android.telephony.TelephonyManager getSubscriberId ": "imse",

    "java.util.Calendar getTimeZone": "location",
    "android.net.wifi.WifiInfo getMacAddress": "mac",
    "android.net.wifi.WifiInfo getMacAddress ": "mac",

    "android.media.MediaRecorder getAudioSource": "media",
    "android.media.MediaRecorder startRecording": "media",
    "android.accounts.AccountManager getPassword": "password",
    "android.telephony.TelephonyManager getLine1Number": "phonenumber",
    "android.hardware.SensorManager getDefaultSensor": "sensor",
    "android.hardware.SensorManager getDefaultSensor ": "sensor",
    "android.telephony.SmsManager sendTextMessage": "sms",
    "android.net.wifi.WifiInfo getSSID": "ssid",
    "android.net.wifi.WifiInfo getSSID ": "ssid",
    "android.accounts.AccountManager getAccounts": "account",
    "android.os.UserManager getUserName": "username",
    "getadvertisingidInfo": "adid",
    "getCellLocation": "location",
    "PhoneLookup": "contact",
    "getLatitude": "location",
    "getLongitude": "location",
    "getLastKnownLocation": "location",
    "requestLocationUpdates": "location",
    "getSimSerialNumber": "sim",
    "getDeviceId": "deviceid",
    "getSubscriberId": "imse",
    "getTimeZone": "location",
    "getMacAddress": "mac",
    "getAudioSource": "media",
    "startRecording": "media",
    "getPassword": "password",
    "getLine1Number": "phonenumber",
    "getDefaultSensor": "sensor",
    "sendTextMessage": "sms",
    "getSSID": "ssid",
    "getAccounts": "account",
    "getUserName": "username"
}


def get_apk_name_map(pp_results_folder):
    apk_name_map = {}
    for i in os.listdir(pp_results_folder):
        if i.startswith('.'):
            continue
        tmp = i.replace('.txt', '').split('_')
        apk_name = '.'.join(tmp[1:])
        apk_name_map[apk_name] = i
    return apk_name_map





if __name__ == '__main__':
    dataflow_folder = "../Results/256app_binary_results/"
    pp_results_folder = "../Results/256app_pp_results"

    #
    TPLListFile = 'TPL_List_Results.txt'
    TPLDataFile = 'TPL_Data_Results.txt'
    TPLListWriter = open(TPLListFile, 'w')
    TPLDataWrite = open(TPLDataFile, 'w')

    # load data flow analysis results
    dataflow_results = {}
    for df in os.listdir(dataflow_folder):
        if df.startswith('.'):
            continue
        apk_name = '.'.join(df.split('.')[:-3])
        df_file = os.path.join(dataflow_folder, df)
        f = open(df_file, 'r')
        content = f.readlines()
        flag = True
        dataflow_results[apk_name] = {}
        for idx, data in enumerate(content):
            if data.startswith('\tPI:'):
                PI = data.split(':')[1]
                TPL_trace = content[idx + 1]
                TPL = TPL_trace.split(':')[1]
                if TPL not in dataflow_results[apk_name]:
                    dataflow_results[apk_name][TPL] = {}
                if PI not in dataflow_results[apk_name][TPL]:
                    dataflow_results[apk_name][TPL][PI] = data.split(' : ')[-1].replace('\n', '') + ' ==> ' + \
                                                          TPL_trace.split(' : ')[-1].replace('\n', '')
    # align the results files' name
    code_pp_name_map = get_apk_name_map(pp_results_folder)
    #
    TPLPack2Name, TPLName2Pack = get_tpl_pack_name_map('./TPL_package_mapping/')

    # init results
    results = {}
    #
    Results_TPL_list_inCode = {}
    Results_TPL_list_notinCode = {}
    Results_TPL_data = {}
    # data sharing with tpl
    for apk_name in dataflow_results:
        td_disclose = 0
        td_notmentioned = 0
        t_disclose = 0
        t_notmentioned = 0
        print(apk_name)
        #

        if len(dataflow_results[apk_name]) > 0 and apk_name in code_pp_name_map:
            results[apk_name] = []
            Results_TPL_data[apk_name] = []
            Results_TPL_list_inCode[apk_name] = []
            Results_TPL_list_notinCode[apk_name] = []
            #
            TPLListWriter.write(apk_name + '\n')
            TPLDataWrite.write(apk_name + '\n')
            # data sharing with tpl
            pp_file = os.path.join(pp_results_folder, code_pp_name_map[apk_name])
            fp = open(pp_file, 'r')
            privacypolicy_results = fp.readlines()
            fp.close()
            ## Problem 1.1 TPL List: identify app's usage of tpl.
            ## ATPChecker can identify the use of TPL in app's code.
            for tpl in dataflow_results[apk_name]:
                TPL_USAGE = False
                for sent in privacypolicy_results:
                    if sent.startswith('\t'):
                        continue
                    if tpl.lower() in sent.lower() or TPL_map[
                        tpl.strip()].lower() in sent.lower():  # the tpl is claimed in the privacy policy

                        ## eliminate abnormal false identification
                        if 'adjust' in tpl or 'com.teamagam.androidslidinguppanel' in tpl or 'activity' in tpl.lower() or tpl.lower() == 'library':
                            if (not 'sdk' in sent.lower()) or (not 'third party' in sent.lower()):
                                continue

                        print("%s claims the use of %s in its privacy policy." % (apk_name, tpl))
                        print("\t Traces of TPL usage in code: %s" % (str(dataflow_results[apk_name][tpl])))
                        print("\t Sentence in %s's privacy policy: %s " % (apk_name, sent))
                        #
                        TPLListWriter.write("\t %s claims the use of %s in its privacy policy.\n" % (apk_name, tpl))
                        TPLListWriter.write(
                            "\t\t Traces of TPL usage in code: %s" % (str(dataflow_results[apk_name][tpl])))
                        TPLListWriter.write("\t\t Sentence in %s's privacy policy: %s \n\n" % (apk_name, sent))
                        TPLListWriter.flush()
                        TPL_USAGE = True
                        # TN. App compliance. ATPChecker identifies the app claims TPL usage in pp.
                        Results_TPL_list_inCode[apk_name].append("{} : {}".format("TN", TPL))
                        break  # successfully identify the TPL usage in app's pp
                if not TPL_USAGE:
                    print("%s does not claims the use of %s in its privacy policy." % (apk_name, tpl))
                    print("\t Traces of TPL usage in code: %s" % str(dataflow_results[apk_name][tpl]))
                    #
                    TPLListWriter.write("\t%s does not claims the use of %s in its privacy policy.\n" % (apk_name, tpl))
                    TPLListWriter.write("\t\t Traces of TPL usage in code: %s\n" % str(dataflow_results[apk_name][tpl]))
                    TPLListWriter.flush()
                    #
                    tmp_tpl = dataflow_results[apk_name]
                    tmp_tpl_data = dataflow_results[apk_name][list(tmp_tpl.keys())[0]]
                    flow = tmp_tpl_data[list(tmp_tpl_data.keys())[0]]

                    #
                    # TP. App non-compliance. ATPChecker identifies the app uses TPL in Code. ATPChecker cannot identify the claims in pp.
                    Results_TPL_list_inCode[apk_name].append("{} : {}".format("TN", TPL))

            ## Problem 1.2 TPL List: identify app's usage of tpl.
            ## App claims the TPL usage in its privacy policy. Check whether ATPChecker identified the usage of TPL in app's code.
            for idx, stmt in enumerate(privacypolicy_results):
                #
                if stmt.startswith('\t'):
                    continue
                for tpl in TPLName2Pack:  # iterate all interested TPLs
                    if tpl.lower() in stmt.lower() or TPLName2Pack[tpl].lower() in stmt.lower():

                        ## eliminate abnormal false identification
                        if 'adjust' in tpl or 'com.teamagam.androidslidinguppanel' in tpl or 'activity' in tpl.lower() or tpl.lower() == 'library':
                            if (not 'sdk' in stmt.lower()) or (not 'third party' in stmt.lower()):
                                continue

                        # TPL claimed in the privacy policy
                        if TPLName2Pack[tpl] in dataflow_results[apk_name]:
                            # TN: App non-compliance. ATPChecker identifies the app claims TPL usage in pp and ientify the usage in Code.
                            print("%s claims the use of %s in its privacy policy." % (apk_name, TPLName2Pack[tpl]))
                            print("\t Traces of TPL usage in code: %s" % (
                                str(dataflow_results[apk_name][TPLName2Pack[tpl]])))
                            print("\t Sentence in %s's privacy policy: %s " % (apk_name, stmt))
                            #
                            TPLListWriter.write(
                                "\t%s claims the use of %s in its privacy policy.\n" % (apk_name, TPLName2Pack[tpl]))
                            TPLListWriter.write("\t\t Traces of TPL usage in code: %s" % (
                                str(dataflow_results[apk_name][TPLName2Pack[tpl]])))
                            TPLListWriter.write("\t\t Sentence in %s's privacy policy: %s \n\n" % (apk_name, stmt))
                            TPLListWriter.flush()
                            Results_TPL_list_notinCode[apk_name].append("{} : {}".format("TN", TPLName2Pack[tpl]))
                        else:
                            if 'org' in tpl.lower() or 'org' in TPLName2Pack[tpl].lower():
                                if ' org ' not in stmt:
                                    continue
                            # FN: App claims TPL usage in pp. ATPChecker cannot identify the usage in Code.
                            print("%s claims the usage of %s in its privacy policy:\n\t\t %s" % (
                                apk_name, TPLName2Pack[tpl], stmt))
                            print("\t ATPchecker doest not identify the use of the TPL in app's Code.\n")
                            #
                            TPLListWriter.write("\t%s claims the usage of %s in its privacy policy:\n\t\t %s" % (
                                apk_name, TPLName2Pack[tpl], stmt))
                            TPLListWriter.write(
                                "\t\t ATPchecker doest not identify the use of the TPL in app's Code.\n")
                            TPLListWriter.flush()
                            #
                            Results_TPL_list_notinCode[apk_name].append("{} : {}".format("FN", TPLName2Pack[tpl]))

            ## Problem 2: TPL data: identify app's data sharing behavior.
            ## ATPChecker identifies the app's data sharing with TPL. Check wheather app claims the usage in app's privacy policy.
            for tpl in dataflow_results[apk_name]:
                TPL_USAGE_FLAG = False
                for idx, c in enumerate(privacypolicy_results):
                    if c.startswith('\t['):
                        stmt = privacypolicy_results[idx - 1]
                        if tpl.lower() in stmt.lower() or TPL_map[
                            tpl.strip()].lower() in stmt.lower():  # The TPL is mentioned in the sentence

                            ## eliminate abnormal false identification
                            if 'adjust' in tpl or 'com.teamagam.androidslidinguppanel' in tpl or 'activity' in tpl.lower() or tpl.lower() == 'library':
                                if (not 'sdk' in stmt.lower()) or ('third party' in stmt.lower()):
                                    continue

                            TPL_USAGE_FLAG = True
                            for data in dataflow_results[apk_name][tpl]:
                                if API2DataMap[data].lower() in c.lower() or API2DataMap[
                                    data].lower() in stmt.lower():  # the data is mentioned in the sentence
                                    td_disclose += 1
                                    if 'sim' in data:
                                        if ' sim ' not in privacypolicy_results[idx - 1]:
                                            continue
                                    print("%s disclose sharing %s with %s is disclosed in the privacy policy. " % (
                                        apk_name, data, tpl))
                                    print("\t\t data trace in code: %s" % (dataflow_results[apk_name][tpl][data]))
                                    print("\t\t Sentence in pp: %s" % (privacypolicy_results[idx - 1]))
                                    #
                                    TPLDataWrite.write(
                                        "\t%s disclose sharing %s with %s is disclosed in the privacy policy. \n" % (
                                            apk_name, data, tpl))
                                    TPLDataWrite.write(
                                        "\t\t\t data trace in code: %s \n" % (dataflow_results[apk_name][tpl][data]))
                                    TPLDataWrite.write("\t\t\t Sentence in pp: %s\n" % (privacypolicy_results[idx - 1]))
                                    TPLDataWrite.flush()
                                    # TN identified. App disclose data sharing with TPL. ATPChecker identified it.
                                    results[apk_name].append('tpl data:' + tpl + ',' + data + ';true')
                                    Results_TPL_data[apk_name].append("TN : {} ==> {}".format(tpl, data))
                                else:
                                    # ATPChecker identifies app's data sharing with TPL without disclosing them in pp.
                                    print("%s misses disclosing sharing %s with %s in its privacy policy." % (
                                        apk_name, data, tpl))
                                    print("\t\t data trace in code: %s" % (dataflow_results[apk_name][tpl][data]))
                                    #
                                    TPLDataWrite.write(
                                        "\t%s misses disclosing sharing %s with %s in its privacy policy.\n" % (
                                            apk_name, data, tpl))
                                    TPLDataWrite.write(
                                        "\t\t\t data trace in code: %s\n" % (dataflow_results[apk_name][tpl][data]))
                                    TPLDataWrite.flush()
                                    # TP identified. App disclose data sharing with TPL without claiming it.
                                    Results_TPL_data[apk_name].append("TP : {} ==> {}".format(tpl, data))
                if not TPL_USAGE_FLAG:
                    # Even TPL not mentioned in app's pp
                    print("%s misses disclosing data sharing with %s in its privacy policy." % (apk_name, tpl))
                    TPLDataWrite.write(
                        "\t%s misses disclosing data sharing with %s in its privacy policy.\n" % (apk_name, tpl))
                    TPLDataWrite.write(
                        "\t\t Traces of data sharing with %s : %s\n" % (tpl, str(dataflow_results[apk_name][tpl])))
                    TPLDataWrite.flush()

                    for data in dataflow_results[apk_name][tpl]:
                        Results_TPL_data[apk_name].append("TP : {} ==> {}".format(tpl, data))

            ## Problem 2: TPL data: identify app's data sharing behavior
            ## ATPChecker identified app's data sharing claims in app's privacy policy. Check whether ATPChecker identifies the usage in app's code
            for idx, stmt in enumerate(privacypolicy_results):
                #
                if not stmt.startswith('\t'):
                    continue
                stmt = stmt[2:-2]
                tmp = stmt.split(',')
                controller = tmp[0].replace('[', '').replace(']', '').replace('\'', '')
                if len(controller) <= 2:
                    continue

                ## eliminate abnormal false identification
                if 'adjust' in controller or 'com.teamagam.androidslidinguppanel' in controller or 'activity' in controller.lower() or controller.lower() == "library":
                    if (not 'sdk' in privacypolicy_results[idx].lower()) or (
                            'third party' in privacypolicy_results[idx].lower()):
                        continue

                if controller.lower() in TPLName2Pack and TPLName2Pack[controller.lower()] in dataflow_results[
                    apk_name]:
                    data = tmp[0].replace('[', '').replace(']', '').replace('\'', '').split(',')
                    for d in data:
                        if d in dataflow_results[apk_name][TPLName2Pack[controller.lower()]]:
                            if 'sim' in d:
                                if ' sim ' not in privacypolicy_results[idx - 1]:
                                    continue
                            TPLDataWrite.write(
                                "\t%s disclose sharing %s with %s is disclosed in the privacy policy. \n" % (
                                    apk_name, d, TPLName2Pack[controller.lower()]))
                            TPLDataWrite.write(
                                "\t\t\t ATPChecker doese not identify the trace in code. \n")
                            TPLDataWrite.write("\t\t\t Sentence in pp: %s\n" % (privacypolicy_results[idx - 1]))
                            TPLDataWrite.flush()

    ###
    for pr in os.listdir(pp_results_folder):
        apk_name = '.'.join(pr.replace('.txt', '').split('_')[1:])
        TPLListWriter.write(apk_name + '\n')
        TPLDataWrite.write(apk_name + '\n')
        if (not apk_name in Results_TPL_data) and (not apk_name in Results_TPL_list_inCode) and (
                not apk_name in Results_TPL_list_notinCode) and (not apk_name in results):
            Results_TPL_list_notinCode[apk_name] = []
            pp_rf = os.path.join(pp_results_folder, pr)
            f = open(pp_rf, 'r')
            privacypolicy_results = f.readlines()
            f.close()
            ## Problem 1.2 TPL List: identify app's usage of tpl.
            ## App claims the TPL usage in its privacy policy. Check whether ATPChecker identified the usage of TPL in app's code.
            for idx, stmt in enumerate(privacypolicy_results):
                #
                if stmt.startswith('\t'):
                    continue
                for tpl in TPLName2Pack:  # iterate all interested TPLs
                    if tpl.lower() in stmt.lower() or TPLName2Pack[tpl].lower() in stmt.lower():
                        ## eliminate abnormal false identification
                        if 'adjust' in tpl or 'com.teamagam.androidslidinguppanel' in tpl or 'activity' in tpl.lower() or tpl.lower() == 'library':
                            if (not 'sdk' in stmt.lower()) or (not 'third party' in stmt.lower()):
                                continue
                        if 'org' in tpl.lower() or 'org' in TPLName2Pack[tpl]:
                            if ' org ' not in stmt:
                                continue
                        # TPL claimed in the privacy policy
                        # FN: App claims TPL usage in pp. ATPChecker cannot identify the usage in Code.
                        print("%s claims the usage of %s in its privacy policy:\n\t\t %s" % (
                            apk_name, TPLName2Pack[tpl], stmt))
                        print("\t ATPchecker doest not identify the use of the TPL in app's Code.\n")
                        #
                        if "{} : {}".format("FN", TPLName2Pack[tpl]) not in Results_TPL_list_notinCode[apk_name]:
                            TPLListWriter.write("\t%s claims the usage of %s in its privacy policy:\n\t\t %s" % (
                                apk_name, TPLName2Pack[tpl], stmt))
                            TPLListWriter.write(
                                "\t\t ATPchecker doest not identify the use of the TPL in app's Code.\n")
                            TPLListWriter.flush()
                            #
                            Results_TPL_list_notinCode[apk_name].append("{} : {}".format("FN", TPLName2Pack[tpl]))

            ## Problem 2: TPL data: identify app's data sharing behavior
            ## ATPChecker identified app's data sharing claims in app's privacy policy. Check whether ATPChecker identifies the usage in app's code
            for idx, tup in enumerate(privacypolicy_results):
                #
                if not tup.startswith('\t'):
                    continue
                tup = tup[2:-2]
                tmp = tup.split(',')
                stmt = privacypolicy_results[idx - 1]
                rt = []
                for tpl in TPLName2Pack:  # iterate all interested TPLs
                    if tpl.lower() in stmt.lower() or TPLName2Pack[tpl].lower() in stmt.lower():
                        ## eliminate abnormal false identification
                        if 'adjust' in tpl or 'com.teamagam.androidslidinguppanel' in tpl or 'activity' in tpl.lower() or tpl.lower() == "library":
                            if not 'third party' in stmt.lower():
                                continue
                        DatainCodeFlag = False
                        TPLinCodeFlag = False
                        for t in dataflow_results[apk_name]:
                            if TPLName2Pack[tpl].lower() in t:
                                TPLinCodeFlag = True
                                for data in dataflow_results[apk_name][t]:
                                    if API2DataMap[data] in stmt.lower():
                                        if '.'.join([apk_name, data, tpl]) not in rt:
                                            if 'sim' in data:
                                                if not ' sim ' in privacypolicy_results[idx - 1]:
                                                    continue
                                            TPLDataWrite.write(
                                                "\t%s disclose sharing %s with %s is disclosed in the privacy policy. \n" % (
                                                    apk_name, data, tpl))
                                            TPLDataWrite.write(
                                                "\t\t\t data trace in code: %s \n" % (
                                                    dataflow_results[apk_name][tpl][data]))
                                            TPLDataWrite.write(
                                                "\t\t\t Sentence in pp: %s\n" % (privacypolicy_results[idx - 1]))
                                            rt.append('.'.join([apk_name, data, tpl]))
                                        DatainCodeFlag = True
                                if not DatainCodeFlag:
                                    if '.'.join([apk_name, data, tpl]) not in rt:
                                        if 'sim' in data:
                                            if not ' sim ' in privacypolicy_results[idx - 1]:
                                                continue
                                        TPLDataWrite.write(
                                            "\t%s disclose sharing %s with %s is disclosed in the privacy policy. \n" % (
                                                apk_name, data, tpl))
                                        TPLDataWrite.write(
                                            "\t\t\t Sentence in pp: %s\n" % (privacypolicy_results[idx - 1]))
                                        TPLDataWrite.write("\t\t\t No Trace found in code \n")
                                        TPLDataWrite.flush()
                                        rt.append('.'.join([apk_name, data, tpl]))
                        if (not TPLinCodeFlag) and (not DatainCodeFlag):
                            for api in API2DataMap:
                                data = API2DataMap[api].lower()
                                if data in stmt:
                                    if 'sim' in data:
                                        if not ' sim ' in data:
                                            continue

                                    if '.'.join([apk_name, data, tpl]) not in rt:
                                        TPLDataWrite.write(
                                            "\t%s disclose sharing %s with %s is disclosed in the privacy policy. \n" % (
                                                apk_name, data, tpl))
                                        TPLDataWrite.write(
                                            "\t\t\t Sentence in pp: %s\n" % (stmt))
                                        TPLDataWrite.write("\t\t\t No Trace found in code \n")
                                        TPLDataWrite.flush()
                                        rt.append('.'.join([apk_name, data, tpl]))
