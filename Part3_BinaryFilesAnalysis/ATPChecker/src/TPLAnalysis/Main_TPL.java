package TPLAnalysis;

import HostAppAnalysis.KzConfig;
import moon.InterProcedureVariableAnalysis;
import soot.*;
import soot.jimple.*;
import soot.jimple.internal.JIdentityStmt;
import soot.jimple.internal.JInstanceFieldRef;
import soot.jimple.internal.JimpleLocalBox;
import soot.jimple.internal.VariableBox;
import soot.toolkits.scalar.UnitValueBoxPair;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;

import static TPLAnalysis.Constant.VERB_NONE_MATCH;
import static TPLAnalysis.Constant.tpl_target_dataset;
import static TPLAnalysis.TPL_Util.checkFolder;
import static TPLAnalysis.TPL_Util.transAar2Jar;
import static TPLAnalysis.ZipUtil.deleteDir;

public class Main_TPL {
    private static String root_results_folder = "./TPL_binary_results";
    private static String tmp_folder = "./tpl_tmp";

    public static void main(String[] args) {
        String root_tpl_folder = "/ATPChecker/dataset/TPL_data";
        File tpl_cate_file = new File(root_tpl_folder);
        File[] tpl_cate_list = tpl_cate_file.listFiles();
        checkFolder(root_results_folder);
        checkFolder(tmp_folder);
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
                System.out.println(tpl.toString());
                File tpl_version_folder = new File(String.valueOf(tpl));
                File[] version_list = tpl_version_folder.listFiles();
                for (File ver : version_list) {
                    if (String.valueOf(ver).endsWith(".DS_Store")) {
                        continue;
                    }
                    //
                    String[] tpl_tmp = tpl.toString().split("/");
                    String tpl_type = tpl_tmp[tpl_tmp.length - 2];
                    String tpl_name = tpl_tmp[tpl_tmp.length - 1];
                    String output_path = root_results_folder + "entrypoints/" + tpl_type + "/" + tpl_name;
                    checkFolder(output_path);
                    String entrypoint_file = output_path + "/entrypoints.txt";
                    String data_flow_file = root_results_folder + "/" + tpl_name + ".txt";

                    if (ver.toString().toLowerCase().contains("com.amazonaws")) {
                        int a = 1;
                    }

                    System.out.println(entrypoint_file);
                    System.out.println(data_flow_file);
                    try {
                        dealSingleTPL(ver, output_path, entrypoint_file, data_flow_file);
                    } catch (Exception e) {
                        System.out.println(e.toString());
                        continue;
                    }
                    break;
                }
            }
        }
    }

    private static void dealSingleTPL(File ver, String output_path, String entrypoint_file, String data_flow_file) throws Exception {
        String[] tmp1 = ver.toString().split("/");
        String TPL_name = tmp1[tmp1.length - 2];
        String results_file = root_results_folder + "/" + TPL_name + ".txt";
        if ((new File(results_file)).exists()) {
            System.out.println("exists!!!  =======  " + results_file);
            return;
        }
        String[] tmp = String.valueOf(ver).split("\\.");
        String tpl_type = tmp[tmp.length - 1];
        // get *.jar file
        String target_file = ver.toString();
        if (tpl_type.equals("aar")) {
            target_file = transAar2Jar(ver, tmp_folder);
        }
        //
        // get entry points
        SootEnvironmentForGraph.init(target_file, KzConfig.platformPath, output_path);
        //
        List<SootMethod> entrypoints = new ArrayList<>();
        BufferedWriter bw = new BufferedWriter(
                new FileWriter(entrypoint_file));
        //
        for (SootClass sootClass : Scene.v().getClasses()) {
            if (sootClass.isInterface() || sootClass.getMethods().size() == 0 || sootClass.isAbstract()) {
                continue;
            }
            for (SootMethod sootMethod : sootClass.getMethods()) {
                if (sootMethod.isPublic() && sootMethod.isConcrete()) {
                    entrypoints.add(sootMethod);
//                    System.out.println(sootMethod.getSignature() + '\n');
                    bw.write(sootMethod.getSignature() + '\n');
                }
            }
        }
        bw.close();
        Scene.v().setEntryPoints(entrypoints);
        BufferedWriter data_flow_writer = new BufferedWriter(
                new FileWriter(data_flow_file));
        for (SootClass sootClass : Scene.v().getClasses()) {
            for (SootMethod sootMethod : sootClass.getMethods()) {
//                Body body = sootMethod.retrieveActiveBody();
                Body body;
                if (!sootMethod.isConcrete()) {
                    continue;
                }
                try {
                    body = sootMethod.retrieveActiveBody();
                } catch (Exception e) {
                    continue;
                }
                PatchingChain<Unit> cUnits = body.getUnits();
                for (Unit unit : cUnits) {
                    String stmt_tmp = unit.toString().toLowerCase();
                    if (((Stmt) unit).containsInvokeExpr()) {
                        String methodname = ((Stmt) unit).getInvokeExpr().getMethodRef().getName().toLowerCase();
                        String classname = ((Stmt) unit).getInvokeExpr().getMethodRef().getDeclaringClass().getName().toLowerCase();
                        boolean flag = false;
                        for (String target_data : tpl_target_dataset) {
                            String[] mtemp = target_data.split(" ");
                            if (classname.contains(mtemp[0].toLowerCase()) && methodname.contains(mtemp[1].toLowerCase())) {//
                                System.out.println(stmt_tmp);
                                flag = true;
                                data_flow_writer.write("stmt:\t" + unit.toString() + "\n");
                                data_flow_writer.write("\t data \t" + target_data + "\n");
                                Local tar_local = null;

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
                                    if (((AssignStmt) unit).getLeftOpBox() instanceof JInstanceFieldRef) {
                                        tar_local = (Local) ((AssignStmt) unit).getRightOpBox().getValue();
                                    } else if (((AssignStmt) unit).getLeftOpBox().getValue() instanceof StaticFieldRef) {
                                        tar_local = (Local) ((AssignStmt) unit).getRightOpBox().getValue();

                                    } else if (((AssignStmt) unit).getLeftOpBox().getValue() instanceof VariableBox) {
                                        tar_local = (Local) ((AssignStmt) unit).getLeftOpBox().getValue();
                                    } else if (((AssignStmt) unit).getLeftOpBox() instanceof VariableBox) {
                                        tar_local = (Local) ((AssignStmt) unit).getLeftOpBox().getValue();
                                    }
                                }
                                List<UnitValueBoxPair> kz_results = InterProcedureVariableAnalysis.findUses(body, (Stmt) unit, tar_local);
                                for (UnitValueBoxPair zunit : kz_results) {
                                    System.out.println("\t === moon out put:\t" + zunit.toString());
                                    data_flow_writer.write("\t\t\t results::\t" + zunit.toString() + "\n");
                                }
                                data_flow_writer.write("\n");
                            }
                        }
                        if (!flag) {
                            for (String target_data : VERB_NONE_MATCH) {
                                if (methodname.contains("get" + target_data) || methodname.contains("request" + target_data)) {
                                    data_flow_writer.write("stmt:\t" + unit.toString() + "\n");
                                    data_flow_writer.write("\t data \t" + target_data + "\n");
                                    Local tar_local = null;

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
                                        if (((AssignStmt) unit).getLeftOpBox() instanceof JInstanceFieldRef) {
                                            tar_local = (Local) ((AssignStmt) unit).getRightOpBox().getValue();
                                        } else if (((AssignStmt) unit).getLeftOpBox().getValue() instanceof StaticFieldRef) {
                                            tar_local = (Local) ((AssignStmt) unit).getRightOpBox().getValue();

                                        } else if (((AssignStmt) unit).getLeftOpBox().getValue() instanceof VariableBox) {
                                            tar_local = (Local) ((AssignStmt) unit).getLeftOpBox().getValue();
                                        } else if (((AssignStmt) unit).getLeftOpBox() instanceof VariableBox) {
                                            tar_local = (Local) ((AssignStmt) unit).getLeftOpBox().getValue();
                                        }
                                    }
                                    List<UnitValueBoxPair> kz_results = InterProcedureVariableAnalysis.findUses(body, (Stmt) unit, tar_local);
                                    for (UnitValueBoxPair zunit : kz_results) {
                                        System.out.println("\t === moon out put:\t" + zunit.toString());
                                        data_flow_writer.write("\t\t\t results::\t" + zunit.toString() + "\n");
                                    }
                                    data_flow_writer.write("\n");
                                }
                            }
                        }
                        data_flow_writer.flush();
                    }
                }
            }
        }
        deleteDir(tmp_folder);
    }
}
