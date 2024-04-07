import os

TARGET_DATA = ["phonenumber",
               "adid", "advertising id", "bluetooth", "contact",
               "email",
               "contact",
               "imei",
               "deviceid",
               "network",
               "sim", "sms", "location", "address", "imse",
               "mac address", "mac",
               "phone number", "ssid", "user credential",
               "username",
               "password", "account",
               "wifi address", "wifi",
               "macaddress",
               "googleadvertiserid",
               "idvertisinginfo",
               "photos"]

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
    "android.telephony.TElephonyManager getDeviceId": "deviceid",
    "android.telephony.TElephonyManager getSimSerialNumber": "sim",
    "android.telephony.TElephonyManager getSubscriberId": "imse",
    "advertisingidClient getInfo": "advertise",
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


def get_tpl_name_map_old(tar_folder):
    kz_map = {}
    for tpl_type in os.listdir(tar_folder):
        f1 = os.path.join(tar_folder, tpl_type)
        if not "DS_Store" in f1:
            f = open(f1, 'r')
            data = f.readlines()
            f.close()
            for d in data:
                tmp = d.replace('\n', '').split(',')
                kz_map[tmp[0] + '.txt'] = tmp[1] + '.txt'
    kz_map['com.mopub.txt'] = "mopub.txt"
    kz_map['com.bingzer.android.ads.txt'] = 'leadbolt.txt'
    kz_map['io.display.txt'] = 'display.io.txt'
    kz_map['org.mozilla.components.txt'] = 'mozilla rhino.txt'
    kz_map['com.tappx.sdk.android.txt'] = 'tappx.txt'
    kz_map['com.mparticle.txt'] = 'kochava.txt'
    kz_map['com.google.firebase.txt'] = 'firebase.txt'
    kz_map['com.pollfish.txt'] = 'pollfish.txt'
    kz_map['com.naver.nid.txt'] = 'naver.txt'
    kz_map['commons-io.txt'] = 'apache apache commons codec.txt'
    kz_map['com.google.ads.mediation.txt'] = 'ironsource.txt'
    kz_map['com.adtoapp.android.txt'] = 'tapsense.txt'
    kz_map['com.facebook.android.txt'] = 'facebook.txt'
    kz_map['com.applovin.txt'] = 'applovin.txt'
    kz_map['com.tencent.mm.opensdk.txt'] = 'wechat.txt'
    kz_map['com.paypal.sdk.txt'] = 'paypal sdk.txt'
    kz_map['com.applovin.mediation.txt'] = 'fyber.txt'
    kz_map['co.adcel.android.txt'] = 'supersonic.txt'
    kz_map['com.clevertap.android.txt'] = 'clevertap.txt'
    kz_map['com.facebook.litho.txt'] = 'litho.txt'
    kz_map['io.intercom.android.txt'] = 'intercom.txt'
    kz_map['com.buzzvil.buzzscreen.txt'] = 'outbrain.txt'
    kz_map['com.noqoush.adfalcon.android.txt'] = 'noqoush adfalcon.txt'
    return kz_map


def get_tpl_name_map(tar_folder):
    kz_map = {}
    for tpl_type in os.listdir(tar_folder):
        f1 = os.path.join(tar_folder, tpl_type)
        if not "DS_Store" in f1:
            f = open(f1, 'r')
            data = f.readlines()
            f.close()
            for d in data:
                tmp = d.replace('\n', '').split(',')
                kz_map[tmp[0]] = tmp[1]
    kz_map['com.mopub'] = "mopub"
    kz_map['com.bingzer.android.ads'] = 'leadbolt'
    kz_map['io.display'] = 'display.io'
    kz_map['org.mozilla.components'] = 'mozilla rhino'
    kz_map['com.tappx.sdk.android'] = 'tappx'
    kz_map['com.mparticle'] = 'kochava'
    kz_map['com.google.firebase'] = 'firebase'
    kz_map['com.pollfish'] = 'pollfish'
    kz_map['com.naver.nid'] = 'naver'
    kz_map['commons-io'] = 'apache apache commons codec'
    kz_map['com.google.ads.mediation'] = 'ironsource'
    kz_map['com.adtoapp.android'] = 'tapsense'
    kz_map['com.facebook.android'] = 'facebook'
    kz_map['com.applovin'] = 'applovin'
    kz_map['com.tencent.mm.opensdk'] = 'wechat'
    kz_map['com.paypal.sdk'] = 'paypal sdk'
    kz_map['com.applovin.mediation'] = 'fyber'
    kz_map['co.adcel.android'] = 'supersonic'
    kz_map['com.clevertap.android'] = 'clevertap'
    kz_map['com.facebook.litho'] = 'litho'
    kz_map['io.intercom.android'] = 'intercom'
    kz_map['com.buzzvil.buzzscreen'] = 'outbrain'
    kz_map['com.noqoush.adfalcon.android'] = 'noqoush adfalcon'
    kz_map['com.adjust.sdk'] = 'adjust'
    kz_map['com.appnexus.opensdk'] = 'appnexus'
    kz_map['com.appsflyer'] = 'appsflyer'
    kz_map['com.criteo.publisher'] = 'criteo'
    kz_map['com.inmobi.monetization'] = 'inmobi'
    kz_map['com.netflix.turbine'] = 'turbin'
    kz_map['com.vdopia.ads.lw'] = 'vdopia'
    kz_map['net.nan21.dnet'] = 'dnet'
    kz_map['org.odpi.egeria'] = 'ocf'
    kz_map['com.netflix.turbine'] = 'turbin'
    kz_map['com.vdopia.ads.lw'] = 'vdopia'
    kz_map['net.nan21.dnet'] = 'dnet'
    kz_map['org.odpi.egeria'] = 'ocf'
    kz_map['android.arch.work'] = 'android workmanager runtime'
    kz_map['bouncycastle'] = 'legion of the bouncy castle java cryptography apis'
    kz_map['ch.acra'] = 'application crash report for android'
    kz_map['com.alipay.sdk'] = 'alipay'
    kz_map['com.bluelinelabs'] = 'conductor'
    kz_map['com.crittercism'] = 'crittercism'
    kz_map['com.evernote'] = 'android job'
    kz_map['com.fasterxml.jackson.core'] = 'jackson databind'
    kz_map['com.github.axet.fbreader'] = 'android fbreader library'
    kz_map['com.github.nisrulz'] = 'easydeviceinfo'
    kz_map['com.google.android.material'] = 'material components for android'
    kz_map['com.google.zxing'] = 'zxing core'
    kz_map['com.ineunet'] = 'knife utilities'
    kz_map['com.jcraft'] = 'jsch'
    kz_map['com.koushikdutta.async'] = 'androidasync'
    kz_map['com.leanplum'] = 'leanplum'
    kz_map['com.nuance'] = 'speechkit'
    kz_map['com.otaliastudios'] = 'cameraview'
    kz_map['com.pubnub'] = 'pubnub'
    kz_map['com.revenuecat.purchases'] = 'revenuecat'
    kz_map['com.rmt.android'] = 'card io'
    kz_map['com.rudderstack.android.integration'] = 'braze'
    kz_map['com.sylversky.library'] = 'sugarorm'
    kz_map['io.sentry'] = 'sentry'
    kz_map['io.vertx'] = 'vert.x core'
    kz_map['org'] = 'jaudiotagger'
    kz_map['org.altbeacon'] = 'altbeacon'
    kz_map['org.apache.commons'] = 'apache commons lang'
    kz_map['org.apache.curator'] = 'curator framework'
    kz_map['org.apache.httpcomponents'] = 'apache httpclient'
    kz_map['org.bouncycastle'] = 'bouncy castle provider'
    kz_map['org.codehaus.groovy'] = 'apache groovy'
    kz_map['org.springframework'] = 'spring testcontext framework'
    kz_map['com.magnet.mmx.ext'] = 'mmx android smack'
    kz_map['com.socialize'] = 'loopy sdk android'
    kz_map['org.twitter4j'] = 'twitter4j'
    return kz_map


def get_tpl_pp_data(results_folder):
    ### privacy policy
    data_type_count = {}
    data_type_sent = {}
    app_info_pp = {}
    for tpl_name in os.listdir(results_folder):
        if "DS_Store" in tpl_name or tpl_name.startswith('.'):
            continue
        file_name = os.path.join(results_folder, tpl_name)
        tpl = tpl_name.lower().replace('.txt', '')
        app_info_pp[tpl] = []
        f = open(file_name, 'r')
        data = ""
        try:
            data = f.readlines()
        except:
            return "Data Not Fully Processed"
        for tmp in data:
            if tmp.startswith('\t'):
                continue
            tmp = tmp.lower()
            for i in TARGET_DATA:
                if i in tmp:
                    app_info_pp[tpl].append(i)
                    if not i in data_type_count:
                        data_type_count[i] = 1
                        data_type_sent[i] = []
                    else:
                        data_type_count[i] += 1
                        data_type_sent[i].append(tmp)
            # print(tmp)
    return app_info_pp


def get_tpl_ss_data(target_folder):
    results = []
    app_info_ss = {}
    for tpl_category in os.listdir(target_folder):
        if 'DS_Store' in tpl_category or tpl_category.startswith('.'): continue
        tpl_name = tpl_category.replace('.txt', '')
        i = tpl_name
        file_name = os.path.join(target_folder, tpl_category)
        if not os.path.exists(file_name):
            continue
        app_info_ss[i.lower()] = []
        f = open(file_name, 'r')
        data = f.readlines()
        f.close()
        for d in data:
            if d.startswith('\t data'):
                t = d.replace('\n', '')
                t = t.replace('\t data \t', '')
                results.append(t)
                app_info_ss[i.lower()].append(t)
    return app_info_ss


#if __name__ == '__main__':
def TPL_compliance_analysis():
    tpl_name_map = get_tpl_name_map('Part4_ResultsGenerator/TPL_package_mapping/')
    app_info_ss_tmp = get_tpl_ss_data('Results/TPL_binary_results')
    app_info_pp_tmp = get_tpl_pp_data('Results/TPL_pp_analysis_results')
    #
    app_info_pp = {}
    # for tpl in app_info_pp_tmp:
    #     if len(app_info_pp_tmp[0]) != 0:
    #         app_info_pp[tpl] = app_info_pp_tmp[tpl]
    app_info_ss = {}
    for tpl in app_info_ss_tmp:
        if len(app_info_ss_tmp[tpl]) > 0:
            app_info_ss[tpl] = app_info_ss_tmp[tpl]
    #
    miss_disclose_compliance = {}
    tpl_no_pp = []
    for tpl_name in app_info_ss:
        name_2 = tpl_name_map[tpl_name].lower()
        if name_2 in app_info_pp:
            ss_data = app_info_ss[tpl_name]
            pp_data = app_info_pp[name_2]
            for i in ss_data:
                if i in pp_data or data_map[i] in pp_data:
                    continue
                else:
                    if tpl_name not in miss_disclose_compliance:
                        miss_disclose_compliance[tpl_name] = []
                    miss_disclose_compliance[tpl_name].append(i)
                    print("%s missing disclose %s in its privacy policy." % (tpl_name, i))
        else:
            tpl_no_pp.append(tpl_name)
    print("TPLs that mis disclose data usage:")
    ret = []
    # for i in miss_disclose_compliance:
    #     print(i)
    ret.append("# TPLs that miss disclosing data usage %d / %d = %f" % (
        len(miss_disclose_compliance), len(app_info_ss), len(miss_disclose_compliance) / len(app_info_ss)))
    print(ret)
    return ret
