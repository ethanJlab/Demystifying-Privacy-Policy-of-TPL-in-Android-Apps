package HostAppAnalysis;

import moon.InterProcedureVariableAnalysis;
import soot.*;
import soot.jimple.*;
import soot.jimple.infoflow.android.manifest.ProcessManifest;
import soot.jimple.infoflow.cmd.Flowdroid;
import soot.jimple.infoflow.memory.FlowDroidTimeoutWatcher;
import soot.jimple.infoflow.results.InfoflowResults;
import soot.jimple.internal.JAssignStmt;
import soot.jimple.internal.JIdentityStmt;
import soot.jimple.internal.JInstanceFieldRef;
import soot.jimple.internal.JimpleLocalBox;
import soot.toolkits.scalar.UnitValueBoxPair;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import static TPLAnalysis.Constant.*;

public class Hostapp_Util {
    public static Object getHostAppDataFlowDestinationNew(String apk_path) throws Exception {
        if (getFileSizeMegaBytes(apk_path) > 100) {
            System.out.println("apk larger than 100 MB" + apk_path);
            return null;
        }
        // initialize parameters and results data structure
        HashMap<String, ArrayList<String>> results_dic = new HashMap<String, ArrayList<String>>();
        boolean flag_pi = false;
        // init flowdroid
        FlowDroidEnvironment.reset();
        FlowDroidEnvironment.init(apk_path, KzConfig.platformPath);
        FlowDroidTimeoutWatcher.timeoutFlag = false;
        int flodroidArgsSize = FlowDroidEnvironment.args.size();
        String[] flowdraoidArgs = new String[flodroidArgsSize];
        FlowDroidEnvironment.args.toArray(flowdraoidArgs);
        ArrayList<InfoflowResults> flowdroidResults = Flowdroid.analyze(flowdraoidArgs);
        if (Flowdroid.exceptionFlag) {
            return null;
        }
        ProcessManifest manifest = null;
        manifest = new ProcessManifest(apk_path);
        String package_name = manifest.getPackageName();
        if (FlowDroidTimeoutWatcher.timeoutFlag) {
            return null;
        }
        // iterate each statement in each method of each classes
        for (SootClass sootClass : Scene.v().getClasses()) {
            for (SootMethod sootMethod : sootClass.getMethods()) {
//                System.out.println("kzmethod:\t"+sootMethod.toString());
                try {
                    if (!sootMethod.isConcrete() || !sootMethod.hasActiveBody()) {
                        continue;
                    }
                    Body body = sootMethod.retrieveActiveBody();
                    // iterate the statements
                    for (Unit unit : body.getUnits()) {
                        if (((Stmt) unit).containsInvokeExpr()) {
                            flag_pi = false;
                            String stmt_raw = unit.toString();
                            String stmt = stmt_raw.toLowerCase();
                            //
                            String methodname = ((Stmt) unit).getInvokeExpr().getMethodRef().getName().toLowerCase();
                            String classname = ((Stmt) unit).getInvokeExpr().getMethodRef().getDeclaringClass().getName().toLowerCase();
                            /* analysis tpl */
                            ArrayList<String> tpl = new ArrayList<>();
                            /* analysis pi */
                            ArrayList<String> pi = new ArrayList<>();

                            for (String pi_pack : host_app_target_dataset) {
                                String[] tmp = pi_pack.split(" ");
                                if (classname.contains(tmp[0].toLowerCase()) && methodname.contains(tmp[1].toLowerCase())) {
//                                if (stmt.contains(pi_pack.toLowerCase())) {
                                    flag_pi = true;
                                    if (!pi.contains(pi_pack + " : " + stmt_raw)) {
                                        pi.add(pi_pack + " : " + stmt_raw);
                                    }
                                    break;
                                }
                            }
                            if (!flag_pi) {
                                for (String pi_pack : VERB_NONE_MATCH) {
                                    if (methodname.contains("get" + pi_pack) || methodname.contains("request" + pi_pack)) {
                                        flag_pi = true;
                                        if (!pi.contains(pi_pack + " : " + stmt_raw)) {
                                            pi.add(pi_pack + " : " + stmt_raw);
                                        }
                                        break;
                                    }
                                }
                            }
                            // get the local for analysis
                            if (flag_pi) {
                                Local tar_local = null;
                                if (unit instanceof IfStmt) {
                                    continue;
                                }
                                if (unit instanceof IdentityStmt) {
                                    tar_local = (Local) ((JIdentityStmt) unit).leftBox.getValue();

                                } else if (unit instanceof InvokeStmt) {
                                    for (ValueBox box : unit.getUseBoxes()) {
                                        if (box instanceof JimpleLocalBox) {
                                            tar_local = (Local) box.getValue();
                                            break;
                                        }
                                    }
                                } else if (unit instanceof AssignStmt) {
                                    if (((AssignStmt) unit).getLeftOpBox().getValue() instanceof StaticFieldRef ||
                                            ((AssignStmt) unit).getLeftOpBox() instanceof JInstanceFieldRef) {
                                        tar_local = (Local) ((AssignStmt) unit).getRightOpBox().getValue();
                                    } else {
                                        tar_local = (Local) ((JAssignStmt) unit).getLeftOpBox().getValue();
                                    }
                                } else {
                                    tar_local = (Local) ((JAssignStmt) unit).getLeftOpBox().getValue();
                                }
                                List<UnitValueBoxPair> results = InterProcedureVariableAnalysis.findUses(
                                        body,
                                        (Stmt) unit,
                                        tar_local);
                                for (UnitValueBoxPair unitValueBoxPair : results) {
                                    System.out.println("\tNothing: " + unitValueBoxPair);
                                    for (String tpl_name : tpl_package_name) {
                                        if (unitValueBoxPair.toString().toLowerCase().contains(tpl_name.toLowerCase())) {
                                            String mykey = stmt_raw + ": TPL :" + tpl_name;
//                                            System.out.println("TPL:" + tpl_name + ": " + unitValueBoxPair.toString());
//                                            System.out.println(stmt_raw + "\n\tTPL:"+tpl_name);
                                            String tpl_stmt = "TPL : " + tpl_name + " : " + unitValueBoxPair.toString();
                                            if (results_dic.containsKey(mykey)) {
                                                StorePIorTPL_NEW(results_dic, flag_pi, true, pi, tpl_stmt, mykey);
                                            } else {
                                                results_dic.put(mykey, new ArrayList<>());
                                                StorePIorTPL_NEW(results_dic, flag_pi, true, pi, tpl_stmt, mykey);
                                            }
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch (Exception e) {
                    System.out.println(e.getMessage());
                }
            }
        }
        return results_dic;
    }

    static void StorePIorTPL_NEW(HashMap<String, ArrayList<String>> results_dic,
                                 boolean flag_pi, boolean flag_tpl,
                                 ArrayList<String> pi_list, String tpl_name_stmt, String stmt) {
        if (flag_pi) {
            for (String pi : pi_list) {
                if ((!results_dic.get(stmt).contains("PI:" + pi))) {
                    results_dic.get(stmt).add("PI:" + pi);
                    System.out.println(stmt);
                    System.out.println("\tPI:" + pi);
                }
            }
        }
        if (flag_tpl) {
            if ((!results_dic.get(stmt).contains(tpl_name_stmt))) {
                results_dic.get(stmt).add(tpl_name_stmt);
                System.out.println("\t" + tpl_name_stmt);
            }
        }
    }

    private static double getFileSizeMegaBytes(String file_name) {
        File file = new File(file_name);
        return (double) file.length() / (1024 * 1024);
    }


    public static void check_dir(String Dir) {
        File targetDir = new File(Dir);
        if (!targetDir.exists())
            targetDir.mkdirs();
    }



    public static List<String> APK_LIST = Arrays.asList(
            "admobileapps.dangdutlawas_apk",
            "admobileapps.djmaimunah_apk",
            "admobileapps.javajazz_apk",
            "air.com.absolutist.match3puzzle.bubblezbubbledefence_apk",
            "air.com.differencegames.hoherecomesthebridefree_apk",
            "air.com.dotpico.poker_apk",
            "air.com.gerwinsoftware.quizpanic_apk",
            "air.com.quicksailor.EscapeBathroom_apk",
            "androidDeveloperJoe.babyTimer_apk",
            "app.diabetes.log_apk",
            "app.quantum.supdate_apk",
            "apps.capricon.BetterSexLife_apk",
            "apps.mobidobi.SexyHotKissingVideos_apk",
            "apps.pawelz.motorcyclesenginessounds_apk",
            "apps.shangria.Bacteria.Vaginosis_apk",
            "badminton.king.sportsgame.smash_apk",
            "be.intotheweb.squeezie_apk",
            "bizomobile.scary.movie.maker_apk",
            "bowtieneck.thunderballchecker_apk",
            "bp.free.puzzle.game.mahjong.onet_apk",
            "br.com.tapps.americanfoodtruck_apk",
            "br.com.tapps.bacteriumevolution_apk",
            "br.com.tapps.californiapizzatruck_apk",
            "br.com.tapps.chicago.burger.truck_apk",
            "br.com.tapps.fashionsalondash_apk",
            "br.com.tapps.foodevolution_apk",
            "br.com.tapps.matchtheemoji_apk",
            "br.com.tapps.mydollhouse_apk",
            "br.com.tapps.mydreamfishtank_apk",
            "br.com.tapps.pressstart_apk",
            "br.com.tapps.topbeautysalon_apk",
            "cloudpandaph.primarkph_apk",
            "cn.cheng.arabicen_apk",
            "cn.cheng.deru_apk",
            "cn.cheng.envi_apk",
            "cn.cheng.rusdict_apk",
            "cn.wps.moffice_eng_apk",
            "color.call.flash.screen.colorphone_apk",
            "com.a802850847516ad2643b9301a.a04550678a_apk",
            "com.aaronclover.sketchescape_apk",
            "com.abc.wheelsonthebusabc_apk",
            "com.abizar.melivideos_apk",
            "com.affinity.rewarded_play_apk",
            "com.agatestudio.ciayostories_apk",
            "com.aim.racing_apk",
            "com.aio.browser.light_apk",
            "com.airkast.KBGGAM_apk",
            "com.airkast.KENZFM_apk",
            "com.airkast.KKFMFM_apk",
            "com.airkast.KSYZFM_apk",
            "com.airkast.MARK_LEVIN_apk",
            "com.airkast.WJQMFM_apk",
            "com.aisle.app_apk",
            "com.al.crimsontide.android_apk",
            "com.alanapps.standoff_apk",
            "com.alawar.straysouls2.free_apk",
            "com.alfa.droplets.gplay_apk",
            "com.amanotes.beathopper_apk",
            "com.amazon.mShop.android.shopping_apk",
            "com.amelosinteractive.snake_apk",
            "com.anddoes.launcher_apk",
            "com.androyal.caloriesguide.ar_apk",
            "com.animedressupgames.chibi_apk",
            "com.animocacollective.google.pandarun1_apk",
            "com.anndconsulting.mancala_apk",
            "com.anndconsulting.tenpinbowling_apk",
            "com.anndconsulting.touchfootball_apk",
            "com.aomatatech.datatransferapp.filesharing_apk",
            "com.ap.advsyra_apk",
            "com.app.akonallsongs_apk",
            "com.app.android.copradar_apk",
            "com.app.weatherclock_apk",
            "com.appeanmoneyonline.freeapp2021_apk",
            "com.appestry.mail_merge_lite_apk",
            "com.appgeneration.itunerclassical_apk",
            "com.appgeneration.itunerfree_apk",
            "com.appgeneration.itunerjazz_apk",
            "com.appgeneration.itunerrelax_apk",
            "com.appgeneration.myalarm_apk",
            "com.appmind.radios.ar_apk",
            "com.appmind.radios.br_apk",
            "com.appmind.radios.co_apk",
            "com.appmind.radios.es_apk",
            "com.appmind.radios.fr_apk",
            "com.appmind.radios.in_apk",
            "com.appmind.radios.it_apk",
            "com.appmind.radios.mx_apk",
            "com.appmind.radios.pe_apk",
            "com.apps21.cursodemaquillaje_apk",
            "com.appster.nikkiguide_apk",
            "com.apptist.alcohol_apk",
            "com.apptist.boardgame_apk",
            "com.apptist.crocodiledentist_apk",
            "com.apptist.drawstraws_apk",
            "com.apptist.luckyroulette.kr_apk",
            "com.apptist.twoplayergames_apk",
            "com.arbstudios.steampunkracer_apk",
            "com.arkhe.batteryrun_apk",
            "com.arkprimalfear.arkprimalsurvival_apk",
            "com.arsanima.olleh_apk",
            "com.asd.europaplustv_apk",
            "com.asiancooking.star.chef.cooking.games_apk",
            "com.asobimo.iruna_en_apk",
            "com.asobimo.iruna_thai_apk",
            "com.athan_apk",
            "com.att.myWireless_apk",
            "com.att.tv_apk",
            "com.autofillwand.kerala_lottery_result_apk",
            "com.avector.itw.itwmj16_apk",
            "com.aws.android_apk",
            "com.axelspringer.tele_apk",
            "com.axitama.sfs.indonesia_apk",
            "com.azinova.crazyfrequency_apk",
            "com.azteca.america_apk",
            "com.badminton.free_apk",
            "com.BakirOmarov.BoxingPhysics_apk",
            "com.bakno.IslandRacerLite_apk",
            "com.bandagames.jigsawquest_apk",
            "com.bandagames.mpuzzle.gp_apk",
            "com.BasicGames.FashionTrends_apk",
            "com.bbk.theme_apk",
            "com.bbmi.jimmy_apk",
            "com.bengali.dictionary.offline_apk",
            "com.bi.slots.immortality_apk",
            "com.bigfishgames.sealedforgottengoog_apk",
            "com.bigflix.bigflixtablet_apk",
            "com.bluemonkeystudio.flexiblerun_apk",
            "com.Born2Play.StackyDash_apk",
            "com.braincrumbz.hangman.lite_apk",
            "com.braindom2riddle_apk",
            "com.brainpub.phonedecor_apk",
            "com.brc.PeriodTrackerDiary_apk",
            "com.briox.riversip.android.tapuz.elections_apk",
            "com.briox.riversip.android.women.sneakers_apk",
            "com.bs.impossible.track.bike.driving.simulator.apps_apk",
            "com.bsbportal.music_apk",
            "com.bsy_web.bookmanager_apk",
            "com.bubadu.bubbu_apk",
            "com.bucap.it_apk",
            "com.buildingcraftinggames.traffic.rider.racer.highway.real.police.motorbike.motor.moto.bike.riding.games.road.racing.asphalt_apk",
            "com.bulky.Yesterday.premium_apk",
            "com.bytetyper.iwantpizza_apk",
            "com.callapp.contacts_apk",
            "com.caller.notes_apk",
            "com.camerasideas.instashot_apk",
            "com.canela.ott_apk",
            "com.cartelapps.tvmxabierta_apk",
            "com.cashingltd.cashing_apk",
            "com.cashngifts_apk",
            "com.cassette.aquapark_apk",
            "com.casualhit.ropeman_apk",
            "com.cbs.app_apk",
            "com.cbs.ca_apk",
            "com.cdi.spiderboy_apk",
            "com.celltick.lockscreen_apk",
            "com.centuryegg.pdm.paid_apk",
            "com.centuryegg.pdm_apk",
            "com.cg.android.babycountdown_apk",
            "com.CharityRun.game_apk",
            "com.chillingo.robberybobfree.android.row_apk",
            "com.chillyroom.smbfan_apk",
            "com.choiceofgames.popcornsodamurder_apk",
            "com.citylive.angers_apk",
            "com.cjoshppingphone_apk",
            "com.claroColombia.contenedor_apk",
            "com.classicshadow.newadventurer_apk",
            "com.cleanmasterx.app_apk",
            "com.cleveland.buckeyes.android_apk",
            "com.cnn.mobile.android.phone_apk",
            "com.codyrotwein.pocketdrums_apk",
            "com.coffeebeanventures.easyvoicerecorder_apk",
            "com.com2us.golfstarworldtour.normal.freefull.google.global.android.common_apk",
            "com.com2us.homerunbattle2.normal.freefull.google.global.android.common_apk",
            "com.companyname.catapult_desert_apk",
            "com.confirmtkt.lite_apk",
            "com.cowboys.star.android_apk",
            "com.craftsman.go_apk",
            "com.craneballs.android.overkill_apk",
            "com.cravecreative.game.pocketpachinko_apk",
            "com.crazylabs.foot.doctor_apk",
            "com.crazylabs.hair.dye.challenge_apk",
            "com.crazylabs.tie.dye.art_apk",
            "com.Create.Your.Own.Unicorn.Dr_apk",
            "com.createspore.forlifesimgamez_apk",
            "com.dailydevotionapp_apk",
            "com.dancingmono.rollingsky_apk",
            "com.dancingskye.rollingsky_apk",
            "com.dankoniyainck.airtvitips_apk",
            "com.darbawirace_apk",
            "com.dariayahuntukabidah.abidahai.kumpulan.sholawat.gus.azmi.mp3.merdu.offline.sholawatgusazmi.islami_apk",
            "com.dc.fcapp.view_apk",
            "com.decoration.furniture.newforminecraft_apk",
            "com.designkeyboard.keyboard_apk",
            "com.Developersoft.spinandwinspinwinner_apk",
            "com.dg.puzzlebrothers.mahjong.catsisland_apk",
            "com.dg.turbonuke.bingo.quest.summer.garden_apk",
            "com.didenko.and.partners.durak_apk",
            "com.digidust.elokence.akinator.freemium_apk",
            "com.directv.dvrscheduler_apk",
            "com.discord_apk",
            "com.dnt7.threeW_apk",
            "com.doapps.android.mln.MLN_1e913e1b06ead0b66e30b6867bf63549_apk",
            "com.doapps.android.mln.MLN_2a3d6d6cc4b5e77238c1fc1bb6cdd681_apk",
            "com.doapps.android.mln.MLN_90d668b2ee3a0975df39f54a3f466090_apk",
            "com.DogHead.Lotto_apk",
            "com.dokebi.dokebi_apk",
            "com.DolphinLiveWallpaper_apk",
            "com.dondeestoy.rob_apk",
            "com.dotscreen.tv5mondeplus.mobile_apk",
            "com.downloadvideo.videodownloadfree21_apk",
            "com.dreamgame.archery.master_apk",
            "com.dreamgame.bubblemania_apk",
            "com.dressup.avatar.vlinder.doll.princess_apk",
            "com.droidhen.turbo_apk",
            "com.dts.freefiremax_apk",
            "com.ducky.bikehill3d_apk",
            "com.dv.adm_apk",
            "com.dvloper.slendrinafree_apk",
            "com.DynamicGames.HeavyBusSimulatorTeste_apk",
            "com.ea.game.pvzfree_row_apk",
            "com.ea.game.realracing2_OTD_na_apk",
            "com.ea.game.realracing2_OTD_row_apk",
            "com.easybrain.block.puzzle.games_apk",
            "com.easygames.race_apk",
            "com.ebnerverlag.feuerwehrmagazin_apk",
            "com.elinasoft.alarmclock_apk",
            "com.english.free_apk",
            "com.enp.client.c.namwon_apk",
            "com.ENP.therings.kr.googleplay_apk",
            "com.eonline.intl.E_apk",
            "com.escape.sindanurazinkaku_apk",
            "com.espn.score_center_apk",
            "com.ezjoynetwork.bubblecandy_apk",
            "com.ezjoynetwork.juicerescue_apk",
            "com.farsight.AndroidPinball.javaProject_apk",
            "com.feelingtouch.sniperzombie_apk",
            "com.fenproductions.faraidh_apk",
            "com.ffcup.tls_apk",
            "com.fgol.HungrySharkEvolutionkorea_apk",
            "com.fgz.flying.fire.truck.engine.rescue.firefighter.robot.games_apk",
            "com.fingersoft.hillclimb_apk",
            "com.fiverr.fiverr_apk",
            "com.fmeddi.meditosd_apk",
            "com.foxygames.carrobotsim_apk",
            "com.france24.androidapp_apk",
            "com.freecraftingadventuregames.crafting.frozen.disney.elsa.mania.party.meetup.dressup.princess.salon.icy.wedding.star.girls_apk",
            "com.frienzyme.a_apk",
            "com.fundevs.app.mediaconverter_apk",
            "com.Funimation.FunimationNow_apk",
            "com.funtomic.dynamons2_apk",
            "com.game.shape.shift_apk",
            "com.gamedesire.poollivepro_apk",
            "com.gamehivecorp.beattheboss3_apk",
            "com.gamepub.bb.g_apk",
            "com.gamesarbica.tabibalsnan_apk",
            "com.gamesforgirlsfree.dressupgames_apk",
            "com.gamesgear.dog.race.stunt.show_apk",
            "com.getone.tonii_apk",
            "com.girlmakeupsalon.fashionfeverstyling_apk",
            "com.goodbarber.amakhaparis_apk",
            "com.goodbarber.inoitips_apk",
            "com.google.android.tts_apk",
            "com.gpakorea.anyenglish_apk",
            "com.greenleaf.android.translator.enja.c_apk",
            "com.gss.cityhighway.stunt.rider_apk",
            "com.gta.grandtheftauto.cheats.five_apk",
            "com.hairclipper.jokeandfunapp21_apk",
            "com.handmark.tweetcaster_apk",
            "com.handsome.menphotoeditor_apk",
            "com.happyadda.jalebi_apk",
            "com.hbi.wdtinc.android.KOB_apk",
            "com.heurehd.projectorhdsplash_apk",
            "com.hltcorp.howardneurology_apk",
            "com.hmallapp_apk",
            "com.hotheadgames.google.bbfootball_apk",
            "com.htc.pitroad_apk",
            "com.hyxen.taximeter.app_apk",
            "com.hz.game.ld2_apk",
            "com.ibragunduz.applockpro_apk",
            "com.innovapp.disenadordecamisetasdefutbol_apk",
            "com.insasofttech.HijabPromDresses_apk",
            "com.insasofttech.subwayrunner_apk",
            "com.iobit.mobilecare_apk",
            "com.iowormzoneio.snakezoneio_apk",
            "com.isandroid.highwayracersvscops_apk",
            "com.j7.j5.j3.j2.j1.wallpapers_apk",
            "com.jakyl.sscfree_apk",
            "com.jiecode.freewaytraffic_apk",
            "com.jjuublihhyi.goaalzawaa_apk",
            "com.kauf.particle.virtualmatch_apk",
            "com.kauf.princessangela2048_apk",
            "com.kauz.android.weather_apk",
            "com.kbjr.android.weather_apk",
            "com.kidsfoodinc.android_make_smoothies_apk",
            "com.kiwigo.magicprincessfashionsalon.free_apk",
            "com.ksmzbrba.two_apk",
            "com.kury.pianotiles2_apk",
            "com.LaFleur.Action.Movie.FX.Maker_apk",
            "com.ldw.fishtycoon2_apk",
            "com.leolegaltechapps.fxvideoeditor_apk",
            "com.lge.lgemembership_apk",
            "com.lgnsd.two_apk",
            "com.macsoftex.portrait_apk",
            "com.mantrapeletpenaklukwanitasejagad.onlineforextrading_apk",
            "com.massagetherapy.bestmassagevideos_apk",
            "com.MediaplayerQ525_apk",
            "com.mersadtm.haram_apk",
            "com.Meteosolutions.Meteo3b_apk",
            "com.mg.potatochipsfarmingsimulator_apk",
            "com.microsoft.skydrive_apk",
            "com.miui.player.apk",
            "com.miui.videoplayer_apk",
            "com.mizmowireless.vvm_apk",
            "com.mizSoftware.cablemovie_apk",
            "com.mobile.numberlocation.gps.callerid_apk",
            "com.mobions.asked_apk",
            "com.motionportrait.ZombieBooth_apk",
            "com.multicraft.game_apk",
            "com.mw.rouletteroyale_apk",
            "com.mypocketgames.cartransportercargoplane_apk",
            "com.nail.art.salon.nuttyapps_apk",
            "com.naynad.nab.resephari_apk",
            "com.nerdcorps.slugthree_apk",
            "com.ninjakiwi.sas3zombieassault_apk",
            "com.nndev.pashtu_stage_shows_apk",
            "com.nokoprint_apk",
            "com.order.kyochonchicken_apk",
            "com.pasia.boltahai_apk",
            "com.peyman.dateconvert_apk",
            "com.photojoinerapp_apk",
            "com.player.farm.lamvuon.farming.nongtrai.farmer.hayfarm.game.bigfarmer_apk",
            "com.PolarBearTeam.RMSingle_apk",
            "com.portalmods.forminecraft_apk",
            "com.project.genina.android.lines_apk",
            "com.race.hedgehogboom_apk",
            "com.radio.station.SMILEY.DJ_apk",
            "com.rallinayamz.rollingsky_apk",
            "com.recipe.filmrise_apk",
            "com.remmaps.thearchersvspigeongame_apk",
            "com.ringtonesforhuawei.freesounds_apk",
            "com.rlk.weathers_apk",
            "com.roa.two_apk",
            "com.RocketGames.Wolfpack_apk",
            "com.samsung.android.scloud_apk",
            "com.samsung.sree_apk",
            "com.sec.spp.push_apk",
            "com.securenetsystems.localx_apk",
            "com.securenetsystems.wsks_apk",
            "com.securenetsystems.wxtq_apk",
            "com.sega.comixzone_apk",
            "com.sega.goldenaxe_apk",
            "com.sega.ristar_apk",
            "com.sega.shinobi_apk",
            "com.sega.streetsofrage.classic_apk",
            "com.sega.streetsofrage2_apk",
            "com.shivarathee.doraemon_apk",
            "com.sigma.naturapps_apk",
            "com.smart.mobile.lin.love.pattern.locker_apk",
            "com.smartedt.edt_apk",
            "com.socialin.android.game.birdlandnew_apk",
            "com.sofeh.android.musicstudio3_apk",
            "com.softick.android.solitaire.klondike_apk",
            "com.sportsseoul.smaglobal.aos_apk",
            "com.springwalk.mediaconverter_apk",
            "com.studyhallentertainment.proATV_apk",
            "com.sundaytoz.kakao.sutda.service_apk",
            "com.Super.Funny.Boomerang.Effect.App_apk",
            "com.tafsirmimpilengkap.forextradingplatform_apk",
            "com.tapinator.taxi.driver.hillstation_apk",
            "com.teamlava.bakerystory_apk",
            "com.teamlava.farmstory_apk",
            "com.teamlava.fashionstory44_apk",
            "com.teamlava.fashionstory45_apk",
            "com.teamlava.fashionstory48_apk",
            "com.teamlava.fashionstory_apk",
            "com.teamlava.petshop_apk",
            "com.teamlava.restaurantstory_apk",
            "com.tekoia.sure.activities_apk",
            "com.tg.eaglebirdcitysimulator2015_apk",
            "com.tgvn.addmesnaps_apk",
            "com.threedos.psalmsofsolomonfree_apk",
            "com.tinyco.futurama_apk",
            "com.together.idlestickman_apk",
            "com.ts.multislot_apk",
            "com.ts.ninewheel_apk",
            "com.tuneonn.shayari_apk",
            "com.ukuland.android_apk",
            "com.vg.truckparking3dfiretruck_apk",
            "com.viacom18.kmofish_apk",
            "com.wallpaper.hai.city_apk",
            "com.wdjt.android.weather_apk",
            "com.webprancer.google.garfieldescapelite_apk",
            "com.week.android.weather_apk",
            "com.whdh.android.weather_apk",
            "com.whsv.android.weather_apk",
            "com.winrgames.bubbleblast_apk",
            "com.winrgames.krazykart_apk",
            "com.winrgames.toweringtiles_apk",
            "com.wonderfulgames.catleosfishhuntwaterrace_apk",
            "com.wpta.android.weather_apk",
            "com.yatzyworld_apk",
            "com.yenimedya.mansetler_apk",
            "com.zaibiminegamescraft.supermonster.bluewhale.shark.game_apk",
            "com.zddapps.hindistatus_apk",
            "com.zingmagic.homerunvfree_apk",
            "darts.king.master.shooting.free_apk",
            "de.afapps.moneyradardetector_apk",
            "exam.upsssc.upsssc_apk",
            "fr.spinbot.lordzio_apk",
            "goldenshorestechnologies.brightestflashlight.free_apk",
            "info.androidx.memocalenf_apk",
            "info.terunuma.chiiku.animedraw_apk",
            "io.blackcandy.probuilder3d_apk",
            "ir.doorbash.backgammon_apk",
            "jp.cloverlab.yurudora_apk",
            "jp.co.anysense.myalbum_apk",
            "jp.co.doublecircle.takarakuji_apk",
            "jp.co.edia.venusblade_apk",
            "jp.co.gagex.odin_apk",
            "jp.co.gakkonet.quizbasicnihonshi2_apk",
            "jp.co.gtndtoc2011_apk",
            "jp.co.liica.otagei_apk",
            "jp.co.netdreamers.umasta_apk",
            "jp.co.otomate.otomatemobile_apk",
            "jp.gree.android.pf.greeapp98_apk",
            "jp.marge.android.wiredecoin2_apk",
            "jp.mbga.a12025983.lite_apk",
            "jp.ne.app.kintai.activity_apk",
            "jp.pascal.cat_apk",
            "jp.seec.sim.moshiano_apk",
            "jp.united.app.kanahei.weightapp_apk",
            "jp.zeroapp.alarm_apk",
            "mmapps.mirror.pro_apk",
            "mobi.infolife.installer_apk",
            "my.photo.picture.keyboard.keyboard.theme_apk",
            "mytown.airport.free_apk",
            "net.lepeng.batterydoctor_apk",
            "net.mumo.music_apk",
            "net.myoji_yurai.myojiOmikuji_apk",
            "net.ptrpg.a11_apk",
            "net.sidebook.dotquest_apk",
            "net.sinovision_apk",
            "net.wyvernware.whosthealien_apk",
            "nl.robertloeberdevelopment_apk",
            "okla.soufiane_apk",
            "org.whiteglow.keepmynotes_apk",
            "pl.cda_apk",
            "pl.pr422.tuner.harmonica_apk",
            "pl.wiocha.app_apk",
            "shamimsoft.ashoora_apk",
            "shamimsoft.ayatolkorsi_apk",
            "teamDoppelGanger.SmarterSubway_apk",
            "truth.or.dare_apk",
            "tv.bangumihyo_apk",
            "uplus.membership_apk",
            "us.pinguo.selfie_apk",
            "videomedia.mp3cutter_apk",
            "videoplayer.videodownloader.hdvideoplayer_apk",
            "wali.juz.amma_apk",
            "zozo.android.crosswords_apk"
    );
}
