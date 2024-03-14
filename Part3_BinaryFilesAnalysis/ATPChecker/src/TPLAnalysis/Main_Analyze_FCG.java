package TPLAnalysis;

import HostAppAnalysis.KzConfig;
import soot.PackManager;
import soot.Scene;
import soot.SootClass;
import soot.SootMethod;
import soot.jimple.toolkits.callgraph.CallGraph;
import soot.jimple.toolkits.callgraph.Edge;

import java.io.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class Main_Analyze_FCG {
    private static String tmp_folder = "tpl_tmp";
    private static String root_tpl_folder = "/Volumes/Samsung8702/ATPChecker_Final_Version/Dataset/TPL_data";
    private static String fcg_save_folder = "./FCG_Compare";


    public static void main(String[] args) throws Exception {
        File tpl_cate_file = new File(root_tpl_folder);
        File[] tpl_cate_list = tpl_cate_file.listFiles();
        String output_path = "test";
        checkFolder(fcg_save_folder);

        // 写文件
        String file_name = "fcg_statistic.csv";
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(file_name));
        bufferedWriter.write("tpl_name,raw_num_node,raw_num_class,raw_num_edge,num_node,num_class,num_edge\n");


        for (File tpl_cate : tpl_cate_list) {
            if (tpl_cate.isFile()) {
                continue;
            }
            File tpl_folder = new File(String.valueOf(tpl_cate));
            File[] tpl_list = tpl_folder.listFiles();
            for (File tpl : tpl_list) {
                if (tpl.isFile()) {
                    continue;
                }
                File tpl_version_folder = new File(String.valueOf(tpl));
                File[] version_list = tpl_version_folder.listFiles();
                boolean TPL_binary = false;
                for (File ver : version_list) {
                    try {
                        if (String.valueOf(ver).endsWith(".DS_Store")) {
                            continue;
                        }
                        String[] tt = String.valueOf(ver).split("/");
                        String tpl_name = tt[tt.length - 2];
                        if (tpl_name.compareTo("net.nao") > 0) {
                            continue;
                        }
                        String[] tmp = String.valueOf(ver).split("\\.");
                        String tpl_type = tmp[tmp.length - 1];
                        String target_file = "";

                        if (tpl_type.equals("aar")) {
                            target_file = transAar2Jar(ver, tmp_folder);
                        } else if (tpl_type.equals("jar")) {
                            target_file = ver.toString();
                        } else if (tpl_type.equals("dex")) {
                            target_file = transDex2Jar(ver, tmp_folder);
                        }

                        SootEnvironmentForGraph.init(target_file, KzConfig.platformPath, output_path);
                        PackManager.v().runPacks();
                        CallGraph cg = Scene.v().getCallGraph();
                        int a = 1;

                        int raw_num_method = Scene.v().getMethodNumberer().size();
                        int raw_num_class = Scene.v().getClassNumberer().size();
                        int raw_num_edge = cg.size();

                        //
                        List<SootMethod> entrypoints = new ArrayList<>();

                        for (SootClass sootClass : Scene.v().getClasses()) {
                            for (SootMethod sootMethod : sootClass.getMethods()) {
                                if (sootMethod.isPublic()) {
                                    entrypoints.add(sootMethod);
//                                System.out.println(sootMethod.getSignature() + '\n');
                                }
                            }
                        }
                        System.out.println(tpl_name);
                        System.out.println("\t writing raw fcg");
                        Scene.v().setEntryPoints(entrypoints);
                        WriteGraph(fcg_save_folder + "/raw",
                                tpl_name + ".txt",
                                cg);

                        try {
                            PackManager.v().runPacks();
                        } catch (Exception e) {
                            continue;
                        }

                        cg = Scene.v().getCallGraph();

                        int num_method = Scene.v().getMethodNumberer().size();
                        int num_class = Scene.v().getClassNumberer().size();
                        int num_edge = cg.size();
                        System.out.println("\t writing new fcg");

                        WriteGraph(fcg_save_folder + "/enhanced",
                                tpl_name + ".txt",
                                cg);

                        int b = 1;
                        bufferedWriter.write(tpl_name + "," + raw_num_method + "," + raw_num_class + "," + raw_num_edge + ","
                                + num_method + "," + num_class + "," + num_edge + "\n");
                        bufferedWriter.flush();
                        System.out.println("kz_log === " + tpl_name + "," + raw_num_method + "," + raw_num_class + "," + raw_num_edge + ","
                                + num_method + "," + num_class + "," + num_edge + "\n");
                    } catch (Exception e) {
                        continue;
                    }
                }
                delete_folder(tmp_folder);
            }
        }
        bufferedWriter.close();
    }

    private static int analyze_FCG_file(String fcg_file) throws IOException {
        HashSet<String> nodes = new HashSet<>();
        File file = new File(fcg_file);
        BufferedReader br = new BufferedReader(new FileReader(file));
        String line = null;
        while ((line = br.readLine()) != null) {
            String caller = line.split(" ==> ")[0].split(" in ")[1];
            String callee = line.split(" ==> ")[1].replace("\n", "");
            nodes.add(caller);
            nodes.add(callee);
        }
        br.close();
        return nodes.size();
    }

    private static boolean delete_folder(String target_folder) {
        File dirFile = new File(target_folder);
        if (!dirFile.exists()) {
            return false;
        }

        if (dirFile.isFile()) {
            return dirFile.delete();
        } else {

            for (File file : dirFile.listFiles()) {
                delete_folder(file.getAbsolutePath());
            }
        }

        return dirFile.delete();

    }


    public static void checkFolder(String folder_name) {
        File tmp = new File(folder_name);
        if (!tmp.exists()) {
            tmp.mkdirs();
        }
    }

    public static String transAar2Jar(File ver, String tmp_folder) {
        checkFolder(tmp_folder);
        ZipUtil.unZip(ver, tmp_folder);
        String jar_file = tmp_folder + "/classes.jar";
        return jar_file;
    }

    public static String transDex2Jar(File ver, String tmp_folder) {
        checkFolder(tmp_folder);
        String target = ver.toString();
        String jar_file = tmp_folder + "/classes.jar";
        String command = "d2j-dex2jar " + target + " -o " + jar_file;
        execShell(command);
        return jar_file;
    }

    public static Process execShell(String shell) {
        Process process = null;
        try {
            process = Runtime.getRuntime().exec(shell);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return process;
    }

    public static void WriteGraph(String save_folder, String filename, CallGraph callGraph) throws IOException {
        checkFolder(save_folder);
        if (new File(save_folder + "/" + filename).exists()) {
            return;
        }
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(save_folder + "/" + filename));

        for (Edge edge : callGraph) {
            bufferedWriter.write(edge + "\n");
            bufferedWriter.flush();
        }
        bufferedWriter.close();
    }
}
