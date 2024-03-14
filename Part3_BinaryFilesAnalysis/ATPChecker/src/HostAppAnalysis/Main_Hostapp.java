package HostAppAnalysis;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Objects;

import static HostAppAnalysis.Hostapp_Util.*;

public class Main_Hostapp {
    public static void main(String[] args) throws Exception {
        String app_path = "/ATPChecker/dataset/host_apk";
        String root_save = "host_app_binary_results";
        check_dir(root_save);
        File app_list = new File(app_path);
        //
        for (File tpl_type : Objects.requireNonNull(app_list.listFiles())) {
            System.out.println(tpl_type);
            if (tpl_type.toString().contains("DS_Store")) {
                continue;
            }
            if (Objects.requireNonNull(tpl_type.listFiles()).length > 0) {
                for (File app_name : Objects.requireNonNull(tpl_type.listFiles())) {
                    if (app_name.toString().contains("DS_Store")) {
                        continue;
                    }
                    HashMap<String, ArrayList<String>> results_dic = new HashMap<String, ArrayList<String>>();
                    String[] kztmp = app_name.toString().split("/");
                    String save_path = root_save + "/" + kztmp[kztmp.length - 1];
                    String results_file = save_path + ".txt";
                    File kz_file = new File(results_file);
                    if (kz_file.exists()) {
                        continue;
                    } else {
                        kz_file.createNewFile();
                    }
                    try {
                        if (app_name.toString().endsWith(".apk")) {
                            System.out.println("kz_apk:" + app_name.toString());
                            results_dic = (HashMap<String, ArrayList<String>>) getHostAppDataFlowDestinationNew(app_name.toString());
                        } else if (app_name.listFiles().length > 0) {
                            File apk = app_name.listFiles()[0];
                            System.out.println("kz_apk:" + apk.toString());
                            results_dic = (HashMap<String, ArrayList<String>>) getHostAppDataFlowDestinationNew(apk.toString());
                        }
                    } catch (Exception e) {
                        System.out.println("error in line 50:" + e.getMessage());
                        continue;
                    }
                    //
                    BufferedWriter data_flow_writer = new BufferedWriter(
                            new FileWriter(results_file));
                    if (results_dic == null) {
                        continue;
                    }
                    for (String key : results_dic.keySet()) {
                        ArrayList<String> tmp = results_dic.get(key);
                        if (tmp.size() > 1) {
                            data_flow_writer.write(key + "\n");
                            for (String k_type : tmp) {
                                data_flow_writer.write("\t" + k_type + "\n");
                            }
                            data_flow_writer.flush();
                        }
                    }
                    data_flow_writer.close();
                }
            }
        }
    }
}
