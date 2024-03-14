# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/5/7
# System: linux

import os

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = 'Courier'

myfont = {
    'family': 'Courier'
}

TPL_map_dict = {
}

data_map = {
    "get_account": "account",
    "email": "email",
    "contact": "contact",
    "advertisingidClient": "adid",
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
    "android.LocationManager requestLocationUpdates": "location",
    "android.location.LocationManager getLongitude": "location",
    "android.telephony.TelephonyManager getSimSerialNumber": "sim",
    "android.telephony.TelephonyManager getDeviceId": "deviceid",
    "android.telephony.TelephonyManager getSubscriberId": "imse",
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


def main(results_folder):
    results = {}
    TPL = []
    PI = []
    data_type = []
    cur_TPL = ''
    for i in os.listdir(results_folder):
        if i .startswith('.'):
            continue
        f1 = os.path.join(results_folder, i)
        if not 'DS_Store' in f1:
            f = open(f1, 'r')
            data = f.readlines()
            f.close()
            if len(data) == 0:
                continue
            ###
            for idx, d in enumerate(data):
                if (not d.startswith('\t')) and (not d.startswith('\n')):
                    if "getMacAddress" in d:
                        a = 1
                    PI_tmp = data[idx + 1]
                    TPL_tmp = data[idx + 2]
                    PI_tmp = PI_tmp.split(' : ')[0].strip().replace('PI:', '')
                    cur_TPL = TPL_tmp.split(' : ')[1].strip()
                    cur_PI = PI_tmp
                    if cur_PI.startswith(' '):
                        cur_PI = cur_PI[1:]
                    cur_PI = data_map[cur_PI]
                    if cur_PI not in PI:
                        PI.append(cur_PI)
                    sig = d.split(':')[-1].replace('\n', '')
                    if cur_TPL not in results:
                        results[cur_TPL] = {}
                    if cur_PI not in results[cur_TPL]:
                        results[cur_TPL][cur_PI] = []
                    results[cur_TPL][cur_PI].append(sig)

    data_statistics = {}
    data2TPL_statistics = {}
    for tpl in results:
        data2TPL_statistics[tpl] = {}
        for data_type in results[tpl]:
            if data_type not in data_statistics:
                data_statistics[data_type] = 1
            data2TPL_statistics[tpl][data_type] = 1
            for stmt in results[tpl][data_type]:
                data_statistics[data_type] += 1
                data2TPL_statistics[tpl][data_type] += 1

    data_statistics = dict(sorted(data_statistics.items(), key=lambda item: item[1], reverse=True))
    # plot figure
    xticks_label = []
    for i in range(9):
        xticks_label.append(list(data_statistics)[i])
    #
    tmp = data2TPL_statistics
    data2TPL_statistics = {}
    for i in data_statistics:
        print('%s:\t%d' % (i, data_statistics[i]))
        data2TPL_statistics[i.strip()] = {}
    for tpl in tmp:
        for dt in tmp[tpl]:
            data2TPL_statistics[dt.strip()][tpl] = tmp[tpl][dt]
    TPL = []
    for d in data2TPL_statistics:
        tmp = dict(sorted(data2TPL_statistics[d].items(), key=lambda item: item[1], reverse=True))
        for t in tmp:
            if t not in TPL:
                TPL.append(t)
        data2TPL_statistics[d] = tmp
    #
    TPL_name_show = []
    for data_t in data2TPL_statistics:
        data_tmp = data2TPL_statistics[data_t]
        s = len(data_tmp)
        if s > 5:
            for i in range(4):
                TPL_name_show.append(list(data_tmp)[i])
        else:
            for i in data_tmp:
                TPL_name_show.append(i)
    #
    TPL_name_show = list(set(TPL_name_show))
    data = []
    # for k in range(len(TPL_name_show)):
    for k in range(len(TPL_name_show)):
        print(TPL_name_show[k])
        tmp = []
        for idx in range(9):
            i = list(data2TPL_statistics)[idx]
            # for i in data2TPL_statistics:
            if TPL_name_show[k] in data2TPL_statistics[i]:
                tmp.append(data2TPL_statistics[i][TPL_name_show[k]])
                print('\t\t%s:\t%d' % (i, data2TPL_statistics[i][TPL_name_show[k]]))
            else:
                tmp.append(0)
        data.append(tmp)

    fig, ax = plt.subplots()
    width = 0.35
    colors = ['#5A9BD5', '#ead1dc', '#EC7D31', '#FFC000', '#84CF53', '#7c2828',
              '#5C92ED', '#9c78bd', '#000000', '#BAB3B3',
              '#5C92EE', '#9c78ba', '#FFFAAA', '#BAB501']
    next_bottom = [0 for i in range(len(data[0]))]
    data_show = data
    for i in range(len(TPL_name_show)):
        ax.bar(xticks_label, data_show[i], width=width, color=colors[i], bottom=next_bottom,
               label=TPL_name_show[i])
        next_bottom = [next_bottom[k] + data_show[i][k] for k in range(len(data_show[i]))]
    leg = ax.legend(prop=myfont)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    ax = plt.gca()
    bwith = 2.5
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)
    plt.grid(zorder=0)
    #
    figure_to_show = [0 for i in range(9)]
    for i in data:
        for d in range(len(i)):
            figure_to_show[d] += i[d]
    index = figure_to_show.copy()
    for i in range(len(figure_to_show)):
        plt.text(i - 0.1, index[i] + 1, figure_to_show[i], fontdict=myfont)
    #
    plt.savefig('./Fig5.pdf')
    plt.show()


if __name__ == '__main__':
    results_folder = '../Results/host_app_binary_results'
    main(results_folder)
