# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/25
# System: linux
import os

data_map = {
    "email": "email",
    "password": "password",
    "network": "network",
    "advertisingidClient getadvertisingidInfo": "adid",
    "advertisingidClient getadInfo": "adid",
    "android.bluetooth.BluetoothAdapter getAddress": "bluetooth",
    "android.telephony.TelephonyManager getCellLocation": "location",
    "android.provider.ContactsContract PhoneLookup": "contact",
    "android.location.Location getLatitude": "location",
    "android.location.Location getLongitude": "location",
    "android.location.LocationManager getLastKnownLocation": "location",
    "android.location.LocationManager requestLocationUpdates": "location",
    "android.location.LocationManager getLongitude": "location",
    "android.telephony.TelephonyManager getSimSerialNumber": "sim",
    "android.telephony.TelephonyManager getDeviceId": "deviceid",
    "android.telephony.TelephonyManager getSubscriberId": "imse",
    "java.util.Calendar getTimeZone": "location",
    "android.net.wifi.WifiInfo getMacAddress": "mac",
    "android.media.MediaRecorder getAudioSource": "media",
    "android.media.MediaRecorder startRecording": "media",
    "android.accounts.AccountManager getPassword": "password",
    "android.telephony.TelephonyManager getLine1Number": "phonenumber",
    "android.hardware.SensorManager getDefaultSensor": "sensor",
    "android.telephony.SmsManager sendTextMessage": "sms",
    "android.net.wifi.WifiInfo getSSID": "ssid",
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

keyword_list = ["email",
                "password",
                "network"]

def get_data_flow_results(results_file):
    ret = ""
    output_list = []
    statistics = {}
    tpl_access_user_data = {}
    trace = {}
    for tpl_type in os.listdir(results_file):
        if '.DS_Store' in tpl_type or tpl_type.startswith('.'): continue
        tpl_folder = os.path.join(results_file, tpl_type)
        # for tpl_name in os.listdir(tpl_folder):
        #     if '.DS_Store' in tpl_name: continue
        #     rf = os.path.join(tpl_folder, tpl_name, "data_flow.txt")
        rf = tpl_folder
        if not os.path.exists(rf): continue
        tpl_name = tpl_type.replace('.txt','')
        f = open(rf, 'r')
        context_tmp = f.readlines()
        for i, line in enumerate(context_tmp):
            if line.startswith('stmt:'):
                tmp = context_tmp[i + 1]
                data_api = tmp.split('\t')[2].replace('\n', '')

                if not data_api in data_map: continue
                data_type = data_map[data_api]
                #
                if data_type in keyword_list and "get" not in line.lower() or "\"" in line:
                    continue
                if data_type not in statistics:
                    statistics[data_type] = []
                statistics[data_type].append(tpl_name)
                print(data_api + '\t' + line)
                output_list.append(data_api + '\t' + line)
                #
                if tpl_name not in tpl_access_user_data:
                    tpl_access_user_data[tpl_name] = []
                tpl_access_user_data[tpl_name].append(data_type + '\t' + line)
                #
                if line not in trace:
                    trace[line] = 0
                trace[line] += 1
    #
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
    for i in tmp:
        print(i)
        output_list.append(i)
        ret += str(i) + " "
    return output_list


# if __name__ == '__main__':
#     TPL_data_flow_results_folder = "../Results/TPL_binary_results"
#     main(TPL_data_flow_results_folder)
