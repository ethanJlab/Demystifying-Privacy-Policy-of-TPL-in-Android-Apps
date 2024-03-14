package HostAppAnalysis;

import soot.G;

import java.util.ArrayList;

public class FlowDroidEnvironment {
    public static ArrayList<String> args;

    public static void reset() {
        args = new ArrayList<String>();
    }

    public static void init(String apkPath, String platformPath) throws Exception {
        // Clean up any old Soot instance we may have
        G.reset();

        // configure Flowdroid arguments
        args.add("-a"); args.add(apkPath);
        args.add("-p"); args.add(platformPath);
        args.add("-s"); args.add(KzConfig.taintFile);
        args.add("-r");
        args.add("-tw"); args.add("NONE");
        args.add("-t"); args.add(KzConfig.wrapperFile);
        args.add("-cp");
        args.add("-d");
        args.add("-ps");
        args.add("-cg"); args.add("SPARK");
        // args.add("-ce"); args.add("NONE");
//        args.add("-w");

        // timeout
        args.add("-dt"); args.add("300"); // seconds
        args.add("-ct"); args.add("300"); // seconds
        args.add("-rt"); args.add("300"); // seconds
    }
}
