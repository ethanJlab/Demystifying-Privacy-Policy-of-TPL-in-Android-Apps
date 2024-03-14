import os

def get_tpl_pack_name_map(tar_folder):
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
    kz_map['com.alipay'] = 'alipay'
    kz_map['com.tencent.bugly'] = 'tencent'
    kz_map['com.bluelinelabs'] = 'conductor'
    kz_map['com.crittercism'] = 'crittercism'
    kz_map['com.evernote'] = 'android job'
    kz_map['com.fasterxml.jackson.core'] = 'jackson databind'
    kz_map['com.github.axet.fbreader'] = 'android fbreader library'
    kz_map['com.github.nisrulz'] = 'easydeviceinfo'
    kz_map['com.google.android.material'] = 'material components for android'
    kz_map['com.google.zxing'] = 'zxing core'
    kz_map['com.umeng.analytics'] = 'umeng'
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
    TPLPack2Name = kz_map
    TPLName2Pack = {}
    for i in kz_map:
        TPLName2Pack[kz_map[i]] = i
    return TPLPack2Name, TPLName2Pack


def get_apk_name_map(pp_results_folder):
    apk_name_map = {}
    for i in os.listdir(pp_results_folder):
        if i.startswith('.'):
            continue
        tmp = i.replace('.txt', '').split('_')
        apk_name = '.'.join(tmp[1:])
        apk_name_map[apk_name] = i
    return apk_name_map


def load_TPL_list_ground_truth(gt_folder):
    TPListGroundTruth = {}
    for i in os.listdir(gt_folder):
        if i.startswith('.'):
            continue
        apk_name = '.'.join(i.split('_')[:-2])
        TPListGroundTruth[apk_name] = []

        f = open(os.path.join(gt_folder, i), 'r')
        context = f.readlines()
        for c in context:
            TPListGroundTruth[apk_name].append(c.replace('\n', ''))
    return TPListGroundTruth


def load_gt():
    f = open(
        './GroundTruth.csv',
        'r')
    content = f.readlines()
    gt = {}
    for i in content:
        if 'AppName,Data' in i: continue
        tmp = i.split(',')
        apk_n = '.'.join(tmp[0].split('.')[:-1])[1:]
        if not apk_n in gt:
            gt[apk_n] = []
        gt[apk_n].append([tmp[1], tmp[2], tmp[3], tmp[4].replace('\n', '')])
    return gt