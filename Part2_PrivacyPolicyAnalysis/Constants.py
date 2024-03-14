# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/4/27
# System: linux

"""
Only using the root word for each verb
"""

SHARE_ACTION = ['protected against', 'distribut', 'trade', 'disclos', 'associat', 'keep', 'accumulat', 'request',
                'sell', 'aggregat', 'chching', 'give', 'track', 'provid', 'sought', 'protecting against', 'obtain',
                'combin', 'possess', 'connect', 'got', 'leas', 'protect against', 'proxi', 'save', 'deliv', 'gave',
                'cach', 'transmit', 'transfer', 'sent', 'rent', 'gather', 'offer', 'afford', 'receiv', 'dissemin',
                'get', 'report', 'sold', 'kept', 'convert', 'share', 'send', 'transport', 'exchang', 'gaven', 'seek',
                'post']

COLLECT_ACTION = ['collect', 'knew', 'gather', 'receiv', 'use', 'know', 'access', 'obtain', 'store', 'save', 'check']

raw_SHARE_ACTION = ['accumulat', 'afford', 'aggregat', 'associat', 'cache', 'chching', 'combin', 'convert', 'connect',
                    'deliver', 'disclose', 'disclosing', 'distribute', 'distributing', 'disseminate', 'disseminating',
                    'exchange', 'exchanging', 'gather', 'get', 'got', 'give', 'giving', 'gave', 'gaven', 'keep', 'kept',
                    'lease', 'leasing', 'obtain', 'offer', 'post', 'possess', 'proxy', 'provide', 'providing',
                    'protect against', 'protected against', 'protecting against', 'receiv', 'receive', 'receiving',
                    'rent', 'report',
                    'request', 'save', 'saving', 'seek', 'sought', 'sell', 'sold', 'share', 'sharing', 'send', 'sent',
                    'track', 'trade', 'trading', 'transport', 'transfer', 'transmit']

raw_COLLECT_ACTION = [
    'access', 'check', 'collect', 'gather', 'know', 'knew', 'obtain', 'receive', 'receiving', 'save', 'saving', 'store',
    'storing', 'use', 'using']

WWWWWH = ['who', 'why', 'when', 'whether', 'what', 'how']

NOT_DATA = ['privacy policy', 'by', 'you']

TPL_LIST = ["AdAd",
            "AdBuddiz",
            "AdColony",
            "AdFlex",
            "AdIQuity",
            "Adjust",
            "AdKnowledge Super Rewards",
            "Adlantis",
            "AdLib",
            "AdMarvel",
            "AdMob",
            "adMost",
            "adPOPcorn",
            "adSage",
            "AdsMogo",
            "adstir",
            "AdWhirl",
            "Adwo",
            "AerServ",
            "AirPush",
            "Amazon Mobile Ads",
            "AmoAd",
            "AppBrain SDK",
            "AppDriver",
            "AppLovin",
            "AppNext",
            "AppNexus",
            "Appodeal",
            "Appsfire",
            "AppsFlyer",
            "Avocarrot",
            "AwesomeAds",
            "Axonix",
            "Bee7",
            "Burstly",
            "BuzzCity",
            "byyd",
            "CallDorado",
            "Cauly Ads",
            "Chartboost",
            "Cheetah Mobile",
            "Conversant",
            "Criteo",
            "Daum ads",
            "Digital Turbine",
            "display.io",
            "domob",
            "DU",
            "Facebook",
            "Flatiron Media",
            "Fractional Media",
            "FreeWheel",
            "Fyber",
            "GetJar",
            "HeyZap",
            "Hunt Mobile Ads",
            "HyprMX",
            "InMobi",
            "Inneractive",
            "Integral Ad Science",
            "Ironsource",
            "Jumptap",
            "Kidoz",
            "Kiip",
            "Kochava",
            "Komli Mobile (aka ZestAdz)",
            "LeadBolt",
            "Lifestreet",
            "Ligatus",
            "LiquidM",
            "LiveRail",
            "Madhouse SmartMAD",
            "Madvertise",
            "MdotM",
            "Medialets",
            "mediba ad",
            "Mediba Admaker",
            "Metaps",
            "Millennial Media",
            "Mintegral",
            "MobClix",
            "Mobeleader",
            "MobFox",
            "MobileAppTracking",
            "mobileCore",
            "MobPartner",
            "MobVista",
            "MobWIN",
            "mOcean",
            "MoPub",
            "MyTarget",
            "NativeX",
            "Nend",
            "Nexage",
            "Nielsen",
            "Noqoush AdFalcon",
            "Ogury",
            "Open Measurement",
            "OpenX",
            "Outbrain",
            "Phunware Advertising",
            "Pocket Change",
            "Pollfish",
            "PubNative",
            "Quattro Wireless Ads",
            "Receptiv",
            "Revmob",
            "Rhythm Premium Mobile Video Advertising",
            "SendDroid",
            "SilverMob",
            "Smaato",
            "Smart AdServer",
            "Sponsorpay",
            "Startapp",
            "Supersonic",
            "Swelen",
            "Taboola",
            "Tap for Tap",
            "Tapcontext",
            "tapcore",
            "Tapdaq",
            "TapIt",
            "Tapjoy",
            "TappX",
            "TapSense",
            "Tenjin",
            "TNK",
            "Unity Ads",
            "Upsight",
            "VDopia",
            "Verve",
            "Video Intelligence",
            "Vpon",
            "VServ",
            "Vungle",
            "WAPS",
            "WapStart.Plus1",
            "WiYun",
            "YouAppi",
            "YouMi",
            "YuMe",
            "AboutLibraries",
            "ACRA",
            "Actionbar Sherlock",
            "ActiveAndroid",
            "Adbrix",
            "Adobe AIR",
            "Alipay",
            "amazon Amazon AWS SDK for Android",
            "Amazon in-app purchasing",
            "Amplitude",
            "AndEngine",
            "Android Activity Saved State",
            "Android Architecture Components",
            "Android Asynchronous Http Client",
            "Android Beacon Library",
            "Android Color Picker",
            "Android Image Cropper",
            "Android Jetpack Annotations",
            "Android Jetpack AppCompat",
            "Android Jetpack core",
            "Android Jetpack Media",
            "Android Jetpack VersionedParcelable",
            "Android Jetpack Widgets",
            "Android Native Plugin for Unity",
            "Android Pull to refresh",
            "Android Support Library collections",
            "Android Support Library Print",
            "Android Support VectorDrawable",
            "Android Transition Support Library",
            "Android View Animations",
            "Android WorkManager",
            "Android YouTube Player",
            "Android-Job",
            "android-multitouch-controller",
            "android-youtubeExtractor",
            "AndroidAsync",
            "AndroidPlot",
            "AndroidSlidingUpPanel",
            "AndroidSVG",
            "AndroidX Activity",
            "AndroidX Cursor Adapter",
            "AndroidX Legacy Support Library core UI",
            "AndroidX Legacy Support Library core utils",
            "AndroidX Loader",
            "AndroidX Local Broadcast Manager",
            "Andromo",
            "apache  Cropper",
            "apache Android In-App Billing Library",
            "apache Apache Commons Codec",
            "apache Apache Commons IO",
            "apache Apache Commons Lang",
            "apache Apache Commons Logging",
            "apache Apache HttpMime API",
            "apache Apache James Mime4j",
            "apache Apache Thrift",
            "apache license Android Query",
            "apache React Native",
            "Appsee",
            "Apptimize",
            "Apsalar",
            "AutoFitTextView",
            "Aviary",
            "AVLoadingIndicatorView",
            "Baidu Geolocation",
            "Basic HTTP Client",
            "BoltsFramework",
            "Bouncer",
            "Box Android API",
            "Braintree Client Encryption Library",
            "Branch",
            "Braze",
            "Butter Knife",
            "CameraView",
            "card.io",
            "Circle Indicator",
            "CircleImageView",
            "CleverTap",
            "Cocos2D-X",
            "CommonsWare Android Components (CWAC)",
            "Comscore Analytics",
            "Conductor",
            "Cordova Google Analytics Plugin",
            "Corona SDK",
            "Countly",
            "Crittercism",
            "Dagger",
            "DBFlow",
            "DevsmartLib",
            "Disk LRU Cache",
            "dnsjava",
            "dom4j",
            "DragSortListView",
            "Dropbox API",
            "EasyDeviceInfo",
            "EasyPermissions",
            "EasyPrefs",
            "Entagged",
            "epublib",
            "facebook AChartEngine",
            "facebook PyTorch",
            "facebook React Native",
            "Fast Android Networking",
            "FastAdapter",
            "FasterXML Jackson",
            "Fetch",
            "Firebase",
            "Flurry Analytics",
            "FMOD Ex Programmers API",
            "Fotoapparat",
            "GameAnalytics",
            "Gamemaker Studio",
            "GeckoView",
            "git Android ViewBadger",
            "git Kin",
            "git Material App Rating",
            "git OpenStreetMap tools for Android",
            "Glide",
            "GNU Kawa",
            "google Android GIF Drawable",
            "google Android Instant Apps",
            "google Android Support Library Async Layout Inflater",
            "google Android Support Library Document File",
            "google Android Support Library v13",
            "google android-wheel",
            "google AndroidX ExifInterface",
            "google AndroidX Multi-Dex Library",
            "google AndroidX Widget ViewPager2",
            "google Chromium",
            "Google Cloud Messaging (GCM)",
            "google Crashlytics",
            "google Crouton",
            "google fabric",
            "google Flutter",
            "google Google Analytics",
            "google Google GData client",
            "google Google Guava",
            "google Google Maps SDK",
            "google Google Play In-app Billing",
            "google Google Play Licensing Service",
            "google Google Protocol Buffers",
            "google Google Protocol Buffers Micro",
            "google Google Protocol Buffers Nano",
            "Google gson",
            "Google Guice",
            "google HttpClient for Android",
            "google Java Native Lua",
            "google javamail-android",
            "google JSON.simple",
            "google juniversalchardet",
            "google libgdx",
            "google Material DateTime Picker",
            "google svg-android",
            "google TensorFlow Lite",
            "google Volley",
            "google YouTube Android Player API",
            "Google ZXing",
            "GravitySnapHelper",
            "greenDAO",
            "greenrobot EventBus",
            "Grpc",
            "HockeyApp",
            "htmlcleaner",
            "HttpClient for AndroidHttpClient for Android",
            "ImageViewZoom",
            "IntelliJ IDEA",
            "Intercom",
            "Ionic Framework",
            "Jackson JSON Processor",
            "JAudiotagger",
            "JavaMail",
            "jchardet",
            "JCraft",
            "JDOM",
            "JetBrains Annotations",
            "Joda",
            "jsoup Java HTML Parser",
            "junit",
            "kObjects Utilities",
            "Konfetti",
            "Kotlin",
            "Krux",
            "Kryo",
            "kSOAP 2",
            "kXML",
            "LeakCanary",
            "Leanplum",
            "LicensesDialog",
            "Litho",
            "Localytics",
            "LoganSquare",
            "Logger",
            "Lottie",
            "Lunar Unity Mobile Console",
            "Mapbox",
            "Marmalade SDK",
            "Material Dialogs",
            "MaterialDrawer",
            "MaterialProgressBar",
            "Matisse",
            "mColorPicker",
            "MessagePack",
            "Milkman Games Extensions",
            "Mitek MiSnap",
            "mixpanel",
            "Moat Analytics",
            "Moga",
            "Moshi",
            "Mozilla Rhino",
            "MPAndroidChart",
            "ms Xamarin",
            "Naver",
            "NeatPlug Unity Plugins",
            "New Relic Mobile",
            "NewQuickActionNewQuickAction3D",
            "Nexage SourceKit-MRAID For Android",
            "NineOldAndroids",
            "Nuance",
            "okHttp",
            "Okio",
            "OneSignal",
            "Open UDID",
            "OpenCensus",
            "OpenIAB",
            "Optimizely",
            "OrmLite",
            "Parse",
            "Paypal SDK",
            "PermissionsDispatcher",
            "PhoneGap  Apache Cordova",
            "PhoneGap Social Sharing",
            "PhotoView",
            "Picasso",
            "prettytime",
            "Prime31 Unity Plugins",
            "PubNub",
            "Pushwoosh",
            "Quantcast",
            "RateThisApp",
            "Reactive Streams",
            "ReactiveX",
            "Realm",
            "RecyclerView Animators",
            "ReLinker",
            "Retrofit",
            "RevenueCat",
            "RootBeer",
            "RoundedImageView",
            "Samsung In-App Purchase",
            "Samsung Pen SDK",
            "Scribe OAuth",
            "Sdkbox",
            "Segment",
            "SendBird",
            "Sentry",
            "ShortcutBadger",
            "SignPost OAuth",
            "Simple DirectMedia Layer",
            "Simple Logging Facade for Java (SLF4J)",
            "Simple XML Serialization",
            "SlidingMenu",
            "Smart App Rate",
            "SmoothProgressBar",
            "Soomla",
            "Speex",
            "Splunk MINT",
            "Spongy Castle - Bouncy Castle for Android",
            "Spring Framework",
            "StickyListHeaders",
            "Stripe",
            "Subsampling scale image view",
            "SugarORM",
            "SwipeRevealLayout",
            "Tablelayout",
            "TagSoup",
            "The Checker Framework",
            "The Java CIFS Client Library (JCIFS)",
            "The Legion of the Bouncy Castle",
            "ThreatMetrix SDK",
            "Timber",
            "uCrop",
            "Umeng",
            "Unity 3D",
            "Universal Image Loader",
            "Urban Airship",
            "ViewPager indicator",
            "ViewPagerExtensions",
            "Visual Studio App Center",
            "Vitamio",
            "XML Pull Parsing",
            "Yandex Metrica",
            "Yoga",
            "ZBar bar code reader",
            "Amazon GameCircle",
            "asmack",
            "BeInToo",
            "Digits for Android",
            "Facebook",
            "Google Play Games Services",
            "HeyZap",
            "JTwitter",
            "Kakao",
            "OpenFeint",
            "Papaya Social",
            "Playhaven",
            "ScoreLoop",
            "Smack API",
            "Snap Bitmoji Kit",
            "Snap Creative Kit",
            "Snap Login Kit",
            "Socialize",
            "swarm",
            "TikTok open SDK",
            "Twitter API ME",
            "Twitter Kit",
            "Twitter4j",
            "VKontakte SDK",
            "WeChat"]
