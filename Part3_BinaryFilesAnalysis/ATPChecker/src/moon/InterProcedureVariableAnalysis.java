package moon;
// copyright moon

import soot.*;
import soot.jimple.*;
import soot.jimple.toolkits.callgraph.CallGraph;
import soot.jimple.toolkits.callgraph.Edge;
import soot.toolkits.graph.BriefUnitGraph;
import soot.toolkits.graph.UnitGraph;
import soot.toolkits.scalar.UnitValueBoxPair;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;

public class InterProcedureVariableAnalysis {
    private static boolean debugMode = false;
    private static String gBanner = "[InterProcedureVariableAnalysis]";

    // ---- //

    // variable definition analysis reversely traverses the method and the callgraph

    public static List<Unit> findDefs(Body body, Stmt stmt, Local local) {
        String lBanner = gBanner + "[findDefs]" + " ";

        HashSet<SootMethod> handledMethods = new HashSet<SootMethod>(); // prevent recursive invocation
        handledMethods.add(body.getMethod());

        CallGraph cg = Scene.v().getCallGraph();
        List<Unit> defs = new ArrayList<Unit>();

        // [1] perform intra-procedure analysis
        List<Unit> intraDefs = IntraProcedureVariableAnalysis.findDefs(body, stmt, local);
        for (Unit intraDef : intraDefs) {
            defs.add(intraDef); // record each intra-definition
            // [2] perform inter-procedure analysis
            // [2-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraDef instanceof IdentityStmt) {
                IdentityStmt identity = (IdentityStmt) intraDef;
                Value identityRop = identity.getRightOp();
                if (!(identityRop instanceof ParameterRef)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-1: Right operator of IdentityStmt is not a ParameterRef instance.");
                        System.out.println(lBanner + "{" + intraDef + "}" + " in " + "{" + intraDef.getTag("SootUnitTag").toString() + "}");
                    }
                    continue;
                }
                ParameterRef paramRef = (ParameterRef) identityRop;
                int paramIdx = paramRef.getIndex();
                SootMethod tgtMethod = body.getMethod();
                Iterator<Edge> edges = cg.edgesInto(tgtMethod); // <-
                while (edges.hasNext()) {
                    Edge edge = edges.next();
                    SootMethod srcMethod = edge.src();
                    if (handledMethods.contains(srcMethod)) {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Recursive invocation happens.");
                            System.out.println(lBanner + "{" + srcMethod.getSignature() + "}" + " " + "will call itself.");
                        }
                        continue;
                    }
                    handledMethods.add(srcMethod);
                    Body srcBody = srcMethod.retrieveActiveBody();
                    Stmt srcStmt = edge.srcStmt();
                    assert srcStmt.containsInvokeExpr(); // sanity check
                    Value srcArg = srcStmt.getInvokeExpr().getArg(paramIdx);
                    if (srcArg instanceof Local) {
                        Local srcLocal = (Local) srcArg;
                        findDefsUtil(srcBody, srcStmt, srcLocal, cg, handledMethods, defs); // almost the same as findDefs(*)
                    } else if (srcArg instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", srcArg.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, srcArg);
                        defs.add(fakeStmt);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Argument of the invocation is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + srcStmt + "}" + " in " + "{" + srcStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
            // [2-2] case: function A(*) { Object obj = B(); } | function B(*) { return obj }
            if (intraDef instanceof AssignStmt && ((AssignStmt) intraDef).containsInvokeExpr()) {
                AssignStmt assign = (AssignStmt) intraDef;
                SootMethod tgtMethod = assign.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-2: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will call itself.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                Body tgtBody = tgtMethod.retrieveActiveBody();
                UnitGraph tgtCfg = new BriefUnitGraph(tgtBody);
                List<Unit> tails = tgtCfg.getTails();
                for (Unit tail : tails) {
                    if (!(tail instanceof ReturnStmt))
                        continue;
                    ReturnStmt tgtStmt = (ReturnStmt) tail;
                    Value tgtValue = tgtStmt.getOp();
                    if (tgtValue instanceof Local) {
                        Local tgtLocal = (Local) tgtValue;
                        findDefsUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, defs); // almost the same as findDefs(*)
                    } else if (tgtValue instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", tgtValue.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, tgtValue);
                        defs.add(fakeStmt);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-2: The returned is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + tgtStmt + "}" + " in " + "{" + tgtStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
        }
        return defs;
    }

    private static void findDefsUtil(Body body, Stmt stmt, Local local,
                                     CallGraph cg, HashSet<SootMethod> handledMethods,
                                     List<Unit> defs) {
        String lBanner = gBanner + "[findDefsUtil]" + " ";

        // [1] perform intra-procedure analysis
        List<Unit> intraDefs = IntraProcedureVariableAnalysis.findDefs(body, stmt, local);
        for (Unit intraDef : intraDefs) {
            defs.add(intraDef); // record each intra-definition
            // [2] perform inter-procedure analysis
            // [2-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraDef instanceof IdentityStmt) {
                IdentityStmt identity = (IdentityStmt) intraDef;
                Value identityRop = identity.getRightOp();
                if (!(identityRop instanceof ParameterRef)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-1: Right operator of IdentityStmt is not a ParameterRef instance.");
                        System.out.println(lBanner + "{" + intraDef + "}" + " in " + "{" + intraDef.getTag("SootUnitTag").toString() + "}");
                    }
                    continue;
                }
                ParameterRef paramRef = (ParameterRef) identityRop;
                int paramIdx = paramRef.getIndex();
                SootMethod tgtMethod = body.getMethod();
                Iterator<Edge> edges = cg.edgesInto(tgtMethod); // <-
                while (edges.hasNext()) {
                    Edge edge = edges.next();
                    SootMethod srcMethod = edge.src();
                    if (handledMethods.contains(srcMethod)) {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Recursive invocation happens.");
                            System.out.println(lBanner + "{" + srcMethod.getSignature() + "}" + " " + "will be called recursively.");
                        }
                        continue;
                    }
                    handledMethods.add(srcMethod);
                    Body srcBody = srcMethod.retrieveActiveBody();
                    Stmt srcStmt = edge.srcStmt();
                    assert srcStmt.containsInvokeExpr(); // sanity check
                    Value srcArg = srcStmt.getInvokeExpr().getArg(paramIdx);
                    if (srcArg instanceof Local) {
                        Local srcLocal = (Local) srcArg;
                        findDefsUtil(srcBody, srcStmt, srcLocal, cg, handledMethods, defs); // almost the same as findDefs(*)
                    } else if (srcArg instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", srcArg.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, srcArg);
                        defs.add(fakeStmt);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Argument of the invocation is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + srcStmt + "}" + " in " + "{" + srcStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
            // [2-2] case: function A(*) { Object obj = B(); } | function B(*) { return obj }
            if (intraDef instanceof AssignStmt && ((AssignStmt) intraDef).containsInvokeExpr()) {
                AssignStmt assign = (AssignStmt) intraDef;
                SootMethod tgtMethod = assign.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-2: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will be called recursively.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                Body tgtBody = tgtMethod.retrieveActiveBody();
                UnitGraph tgtCfg = new BriefUnitGraph(tgtBody);
                List<Unit> tails = tgtCfg.getTails();
                for (Unit tail : tails) {
                    if (!(tail instanceof ReturnStmt))
                        continue;
                    ReturnStmt tgtStmt = (ReturnStmt) tail;
                    Value tgtValue = tgtStmt.getOp();
                    if (tgtValue instanceof Local) {
                        Local tgtLocal = (Local) tgtValue;
                        findDefsUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, defs); // almost the same as findDefs(*)
                    } else if (tgtValue instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", tgtValue.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, tgtValue);
                        defs.add(fakeStmt);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-2: The returned is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + tgtStmt + "}" + " in " + "{" + tgtStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
        }
    }

    // ---- //

    // variable use analysis reversely traverses the method and the callgraph to find variable definitions,
    // and then, it forwardly traverses the method and the callgraph to find variable uses.

    public static List<UnitValueBoxPair> findUses(Body body, Stmt stmt, Local local) {
        String lBanner = gBanner + "[findUses]" + " ";

        HashSet<SootMethod> handledMethods = new HashSet<SootMethod>(); // prevent recursive invocation
        handledMethods.add(body.getMethod());

        CallGraph cg = Scene.v().getCallGraph();
        List<UnitValueBoxPair> uses = new ArrayList<UnitValueBoxPair>();

        // [1] perform inter-procedure analysis (backward)
        List<Unit> intraDefs = IntraProcedureVariableAnalysis.findDefs(body, stmt, local);
        for (Unit intraDef : intraDefs) {
            // [1-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraDef instanceof IdentityStmt) {
                IdentityStmt identity = (IdentityStmt) intraDef;
                Value identityRop = identity.getRightOp();
                if (!(identityRop instanceof ParameterRef)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-1: Right operator of IdentityStmt is not a ParameterRef instance.");
                        System.out.println(lBanner + "{" + intraDef + "}" + " in " + "{" + intraDef.getTag("SootUnitTag").toString() + "}");
                    }
                    continue;
                }
                ParameterRef paramRef = (ParameterRef) identityRop;
                int paramIdx = paramRef.getIndex();
                SootMethod tgtMethod = body.getMethod();
                Iterator<Edge> edges = cg.edgesInto(tgtMethod); // <-
                while (edges.hasNext()) {
                    Edge edge = edges.next();
                    SootMethod srcMethod = edge.src();
                    if (handledMethods.contains(srcMethod)) {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Recursive invocation happens.");
                            System.out.println(lBanner + "{" + srcMethod.getSignature() + "}" + " " + "will call itself.");
                        }
                        continue;
                    }
                    handledMethods.add(srcMethod);
                    Body srcBody = srcMethod.retrieveActiveBody();
                    Stmt srcStmt = edge.srcStmt();
                    Value srcArg = srcStmt.getInvokeExpr().getArg(paramIdx);
                    if (srcArg instanceof Local) {
                        Local srcLocal = (Local) srcArg;
                        findUsesBckwardUtil(srcBody, srcStmt, srcLocal, cg, handledMethods, uses);
                    } else if (srcArg instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", srcArg.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, srcArg);
                        ValueBox fakeValueBox = fakeStmt.getLeftOpBox();
                        UnitValueBoxPair pair = new UnitValueBoxPair(fakeStmt, fakeValueBox);
                        uses.add(pair);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Argument of the invocation is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + srcStmt + "}" + " in " + "{" + srcStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
            // [1-2] case: function A(*) { Object obj = B(); } | function B(*) { return obj }
            if (intraDef instanceof AssignStmt && ((AssignStmt) intraDef).containsInvokeExpr()) {
                AssignStmt assign = (AssignStmt) intraDef;
                SootMethod tgtMethod = assign.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-2: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will call itself.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                Body tgtBody = tgtMethod.retrieveActiveBody();
                UnitGraph tgtCfg = new BriefUnitGraph(tgtBody);
                List<Unit> tails = tgtCfg.getTails();
                for (Unit tail : tails) {
                    if (!(tail instanceof ReturnStmt))
                        continue;
                    ReturnStmt tgtStmt = (ReturnStmt) tail;
                    Value tgtValue = tgtStmt.getOp();
                    if (tgtValue instanceof Local) {
                        Local tgtLocal = (Local) tgtValue;
                        findUsesBckwardUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, uses);
                    } else if (tgtValue instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", tgtValue.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, tgtValue);
                        ValueBox fakeValueBox = fakeStmt.getLeftOpBox();
                        UnitValueBoxPair pair = new UnitValueBoxPair(fakeStmt, fakeValueBox);
                        uses.add(pair);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-2: The returned is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + tgtStmt + "}" + " in " + "{" + tgtStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
        }
        // [2] perform intra-procedure analysis
        List<UnitValueBoxPair> intraUses = IntraProcedureVariableAnalysis.findUses(body, stmt, local); // *
        for (UnitValueBoxPair pair : intraUses) {
            Stmt intraUse = (Stmt) pair.unit;
            uses.add(pair); // record each intra-use
            // [3] perform inter-procedure analysis (forward)
            // [3-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraUse.containsInvokeExpr()) {
                if (intraUse instanceof AssignStmt)
                    if (pair.getValueBox() == ((AssignStmt) intraUse).getLeftOpBox())
                        continue;

                SootMethod tgtMethod = intraUse.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-3: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will call itself.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                int argIdx = -1;
                for (int idx = 0; idx < intraUse.getInvokeExpr().getArgCount(); idx++) {
                    ValueBox vb = intraUse.getInvokeExpr().getArgBox(idx);
                    if (pair.getValueBox() == vb)
                        argIdx = idx;
                }
                Body tgtBody = tgtMethod.retrieveActiveBody();
                Stmt tgtStmt = null;
                Local tgtLocal = null;
                for (Unit u : tgtBody.getUnits()) {
                    if (argIdx == -1) {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ThisRef) {
                            tgtStmt = (Stmt) u;
                            tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                        }
                    } else {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ParameterRef) {
                            if (((ParameterRef) ((IdentityStmt) u).getRightOp()).getIndex() == argIdx) {
                                tgtStmt = (Stmt) u;
                                tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                            }
                        }
                    }
                    if (tgtStmt != null || tgtLocal != null)
                        break;
                }
                if (tgtStmt == null || tgtLocal == null)
                    continue;
                findUsesForwardUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, uses);
            }
        }

        return uses;
    }

    public static List<UnitValueBoxPair> findUsesBckward(Body body, Stmt stmt, Local local) {
        String lBanner = gBanner + "[findUsesBackward]" + " ";

        HashSet<SootMethod> handledMethods = new HashSet<SootMethod>(); // prevent recursive invocation
        handledMethods.add(body.getMethod());

        CallGraph cg = Scene.v().getCallGraph();
        List<UnitValueBoxPair> uses = new ArrayList<UnitValueBoxPair>();

        // [1] perform inter-procedure analysis (backward)
        List<Unit> intraDefs = IntraProcedureVariableAnalysis.findDefs(body, stmt, local);
        for (Unit intraDef : intraDefs) {
            // [1-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraDef instanceof IdentityStmt) {
                IdentityStmt identity = (IdentityStmt) intraDef;
                Value identityRop = identity.getRightOp();
                if (!(identityRop instanceof ParameterRef)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-1: Right operator of IdentityStmt is not a ParameterRef instance.");
                        System.out.println(lBanner + "{" + intraDef + "}" + " in " + "{" + intraDef.getTag("SootUnitTag").toString() + "}");
                    }
                    continue;
                }
                ParameterRef paramRef = (ParameterRef) identityRop;
                int paramIdx = paramRef.getIndex();
                SootMethod tgtMethod = body.getMethod();
                Iterator<Edge> edges = cg.edgesInto(tgtMethod); // <-
                while (edges.hasNext()) {
                    Edge edge = edges.next();
                    SootMethod srcMethod = edge.src();
                    if (handledMethods.contains(srcMethod)) {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Recursive invocation happens.");
                            System.out.println(lBanner + "{" + srcMethod.getSignature() + "}" + " " + "will call itself.");
                        }
                        continue;
                    }
                    handledMethods.add(srcMethod);
                    Body srcBody = srcMethod.retrieveActiveBody();
                    Stmt srcStmt = edge.srcStmt();
                    Value srcArg = srcStmt.getInvokeExpr().getArg(paramIdx);
                    if (srcArg instanceof Local) {
                        Local srcLocal = (Local) srcArg;
                        findUsesBckwardUtil(srcBody, srcStmt, srcLocal, cg, handledMethods, uses);
                    } else if (srcArg instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", srcArg.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, srcArg);
                        ValueBox fakeValueBox = fakeStmt.getLeftOpBox();
                        UnitValueBoxPair pair = new UnitValueBoxPair(fakeStmt, fakeValueBox);
                        uses.add(pair);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Argument of the invocation is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + srcStmt + "}" + " in " + "{" + srcStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
            // [1-2] case: function A(*) { Object obj = B(); } | function B(*) { return obj }
            if (intraDef instanceof AssignStmt && ((AssignStmt) intraDef).containsInvokeExpr()) {
                AssignStmt assign = (AssignStmt) intraDef;
                SootMethod tgtMethod = assign.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-2: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will call itself.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                Body tgtBody = tgtMethod.retrieveActiveBody();
                UnitGraph tgtCfg = new BriefUnitGraph(tgtBody);
                List<Unit> tails = tgtCfg.getTails();
                for (Unit tail : tails) {
                    if (!(tail instanceof ReturnStmt))
                        continue;
                    ReturnStmt tgtStmt = (ReturnStmt) tail;
                    Value tgtValue = tgtStmt.getOp();
                    if (tgtValue instanceof Local) {
                        Local tgtLocal = (Local) tgtValue;
                        findUsesBckwardUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, uses);
                    } else if (tgtValue instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", tgtValue.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, tgtValue);
                        ValueBox fakeValueBox = fakeStmt.getLeftOpBox();
                        UnitValueBoxPair pair = new UnitValueBoxPair(fakeStmt, fakeValueBox);
                        uses.add(pair);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-2: The returned is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + tgtStmt + "}" + " in " + "{" + tgtStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
        }
        // [2] perform intra-procedure analysis
        List<UnitValueBoxPair> intraUses = IntraProcedureVariableAnalysis.findUsesBckward(body, stmt, local); // *
        for (UnitValueBoxPair pair : intraUses) {
            Stmt intraUse = (Stmt) pair.unit;
            uses.add(pair); // record each intra-use
            // [3] perform inter-procedure analysis (forward)
            // [3-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraUse.containsInvokeExpr()) {
                if (intraUse instanceof AssignStmt)
                    if (pair.getValueBox() == ((AssignStmt) intraUse).getLeftOpBox())
                        continue;

                SootMethod tgtMethod = intraUse.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-3: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will call itself.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                int argIdx = -1;
                for (int idx = 0; idx < intraUse.getInvokeExpr().getArgCount(); idx++) {
                    ValueBox vb = intraUse.getInvokeExpr().getArgBox(idx);
                    if (pair.getValueBox() == vb)
                        argIdx = idx;
                }
                Body tgtBody = tgtMethod.retrieveActiveBody();
                Stmt tgtStmt = null;
                Local tgtLocal = null;
                for (Unit u : tgtBody.getUnits()) {
                    if (argIdx == -1) {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ThisRef) {
                            tgtStmt = (Stmt) u;
                            tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                        }
                    } else {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ParameterRef) {
                            if (((ParameterRef) ((IdentityStmt) u).getRightOp()).getIndex() == argIdx) {
                                tgtStmt = (Stmt) u;
                                tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                            }
                        }
                    }
                    if (tgtStmt != null || tgtLocal != null)
                        break;
                }
                if (tgtStmt == null || tgtLocal == null)
                    continue;
                findUsesForwardUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, uses);
            }
        }

        return uses;
    }

    public static List<UnitValueBoxPair> findUsesForward(Body body, Stmt stmt, Local local) {
        String lBanner = gBanner + "[findUsesForward]" + " ";

        HashSet<SootMethod> handledMethods = new HashSet<SootMethod>(); // prevent recursive invocation
        handledMethods.add(body.getMethod());

        CallGraph cg = Scene.v().getCallGraph();
        List<UnitValueBoxPair> uses = new ArrayList<UnitValueBoxPair>();

        // [1] perform intra-procedure analysis
        List<UnitValueBoxPair> intraUses = IntraProcedureVariableAnalysis.findUsesForward(body, stmt, local); // *
        for (UnitValueBoxPair pair : intraUses) {
            Stmt intraUse = (Stmt) pair.unit;
            uses.add(pair); // record each intra-use
            // [2] perform inter-procedure analysis (forward)
            // [2-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraUse.containsInvokeExpr()) {
                if (intraUse instanceof AssignStmt)
                    if (pair.getValueBox() == ((AssignStmt) intraUse).getLeftOpBox())
                        continue;

                SootMethod tgtMethod = intraUse.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-1: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will call itself.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                int argIdx = -1;
                for (int idx = 0; idx < intraUse.getInvokeExpr().getArgCount(); idx++) {
                    ValueBox vb = intraUse.getInvokeExpr().getArgBox(idx);
                    if (pair.getValueBox() == vb)
                        argIdx = idx;
                }
                Body tgtBody = tgtMethod.retrieveActiveBody();
                Stmt tgtStmt = null;
                Local tgtLocal = null;
                for (Unit u : tgtBody.getUnits()) {
                    if (argIdx == -1) {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ThisRef) {
                            tgtStmt = (Stmt) u;
                            tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                        }
                    } else {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ParameterRef) {
                            if (((ParameterRef) ((IdentityStmt) u).getRightOp()).getIndex() == argIdx) {
                                tgtStmt = (Stmt) u;
                                tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                            }
                        }
                    }
                    if (tgtStmt != null || tgtLocal != null)
                        break;
                }
                if (tgtStmt == null || tgtLocal == null)
                    continue;
                findUsesForwardUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, uses);
            }
        }

        return uses;
    }

    private static void findUsesBckwardUtil(Body body,
                                            Stmt stmt, Local local, CallGraph cg,
                                            HashSet<SootMethod> handledMethods,
                                            List<UnitValueBoxPair> uses) {
        String lBanner = gBanner + "[findUsesBckwardUtil]" + " ";

        // [1] perform inter-procedure analysis (backward)
        List<Unit> intraDefs = IntraProcedureVariableAnalysis.findDefs(body, stmt, local);
        for (Unit intraDef : intraDefs) {
            // [1-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraDef instanceof IdentityStmt) {
                IdentityStmt identity = (IdentityStmt) intraDef;
                Value identityRop = identity.getRightOp();
                if (!(identityRop instanceof ParameterRef)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-1: Right operator of IdentityStmt is not a ParameterRef instance.");
                        System.out.println(lBanner + "{" + intraDef + "}" + " in " + "{" + intraDef.getTag("SootUnitTag").toString() + "}");
                    }
                    continue;
                }
                ParameterRef paramRef = (ParameterRef) identityRop;
                int paramIdx = paramRef.getIndex();
                SootMethod tgtMethod = body.getMethod();
                Iterator<Edge> edges = cg.edgesInto(tgtMethod); // <-
                while (edges.hasNext()) {
                    Edge edge = edges.next();
                    SootMethod srcMethod = edge.src();
                    if (handledMethods.contains(srcMethod)) {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Recursive invocation happens.");
                            System.out.println(lBanner + "{" + srcMethod.getSignature() + "}" + " " + "will be called recursively.");
                        }
                        continue;
                    }
                    handledMethods.add(srcMethod);
                    Body srcBody = srcMethod.retrieveActiveBody();
                    Stmt srcStmt = edge.srcStmt();
                    Value srcArg = srcStmt.getInvokeExpr().getArg(paramIdx);
                    if (srcArg instanceof Local) {
                        Local srcLocal = (Local) srcArg;
                        findUsesBckwardUtil(srcBody, srcStmt, srcLocal, cg, handledMethods, uses);
                    } else if (srcArg instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", srcArg.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, srcArg);
                        ValueBox fakeValueBox = fakeStmt.getLeftOpBox();
                        UnitValueBoxPair pair = new UnitValueBoxPair(fakeStmt, fakeValueBox);
                        uses.add(pair);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-1: Argument of the invocation is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + srcStmt + "}" + " in " + "{" + srcStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
            // [1-2] case: function A(*) { Object obj = B(); } | function B(*) { return obj }
            if (intraDef instanceof AssignStmt && ((AssignStmt) intraDef).containsInvokeExpr()) {
                AssignStmt assign = (AssignStmt) intraDef;
                SootMethod tgtMethod = assign.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-2: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will be called recursively.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                Body tgtBody = tgtMethod.retrieveActiveBody();
                UnitGraph tgtCfg = new BriefUnitGraph(tgtBody);
                List<Unit> tails = tgtCfg.getTails();
                for (Unit tail : tails) {
                    if (!(tail instanceof ReturnStmt))
                        continue;
                    ReturnStmt tgtStmt = (ReturnStmt) tail;
                    Value tgtValue = tgtStmt.getOp();
                    if (tgtValue instanceof Local) {
                        Local tgtLocal = (Local) tgtValue;
                        findUsesBckwardUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, uses);
                    } else if (tgtValue instanceof Constant) {
                        Local fakeLocal = Jimple.v().newLocal("fakeLocal", tgtValue.getType());
                        AssignStmt fakeStmt = Jimple.v().newAssignStmt(fakeLocal, tgtValue);
                        ValueBox fakeValueBox = fakeStmt.getLeftOpBox();
                        UnitValueBoxPair pair = new UnitValueBoxPair(fakeStmt, fakeValueBox);
                        uses.add(pair);
                    } else {
                        if (debugMode) {
                            System.out.println(lBanner + "CASE-2: The returned is not a constant value or a local variable.");
                            System.out.println(lBanner + "{" + tgtStmt + "}" + " in " + "{" + tgtStmt.getTag("SootUnitTag").toString() + "}");
                        }
                        continue;
                    }
                }
            }
        }
        // [2] perform intra-procedure analysis
        List<UnitValueBoxPair> intraUses = IntraProcedureVariableAnalysis.findUsesBckward(body, stmt, local); // *
        for (UnitValueBoxPair pair : intraUses)
            uses.add(pair); // record each intra-use
    }

    private static void findUsesForwardUtil(Body body, Stmt stmt,
                                            Local local, CallGraph cg,
                                            HashSet<SootMethod> handledMethods,
                                            List<UnitValueBoxPair> uses) {
        String lBanner = gBanner + "findUsesForwardUtil" + " ";

        // [1] perform intra-procedure analysis
        List<UnitValueBoxPair> intraUses = IntraProcedureVariableAnalysis.findUsesForward(body, stmt, local); // *
        for (UnitValueBoxPair pair : intraUses) {
            Stmt intraUse = (Stmt) pair.unit;
            uses.add(pair); // record each intra-use
            // [2] perform inter-procedure analysis (forward)
            // [2-1] case: function A(*) { Object obj = *; B(obj); } | function B(*) { use obj }
            if (intraUse.containsInvokeExpr()) {
                if (intraUse instanceof AssignStmt)
                    if (pair.getValueBox() == ((AssignStmt) intraUse).getLeftOpBox())
                        continue;

                SootMethod tgtMethod = intraUse.getInvokeExpr().getMethod();
                if (handledMethods.contains(tgtMethod)) {
                    if (debugMode) {
                        System.out.println(lBanner + "CASE-1: Recursive invocation happens.");
                        System.out.println(lBanner + "{" + tgtMethod.getSignature() + "}" + " " + "will be called recursively.");
                    }
                    continue;
                }
                if (!tgtMethod.isConcrete())
                    continue;
                handledMethods.add(tgtMethod);
                int argIdx = -1;
                for (int idx = 0; idx < intraUse.getInvokeExpr().getArgCount(); idx++) {
                    ValueBox vb = intraUse.getInvokeExpr().getArgBox(idx);
                    if (pair.getValueBox() == vb)
                        argIdx = idx;
                }
                Body tgtBody = tgtMethod.retrieveActiveBody();
                Stmt tgtStmt = null;
                Local tgtLocal = null;
                for (Unit u : tgtBody.getUnits()) {
                    if (argIdx == -1) {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ThisRef) {
                            tgtStmt = (Stmt) u;
                            tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                        }
                    } else {
                        if (u instanceof IdentityStmt && ((IdentityStmt) u).getRightOp() instanceof ParameterRef) {
                            if (((ParameterRef) ((IdentityStmt) u).getRightOp()).getIndex() == argIdx) {
                                tgtStmt = (Stmt) u;
                                tgtLocal = (Local) ((IdentityStmt) u).getLeftOp();
                            }
                        }
                    }
                    if (tgtStmt != null || tgtLocal != null)
                        break;
                }
                if (tgtStmt == null || tgtLocal == null)
                    continue;
                findUsesForwardUtil(tgtBody, tgtStmt, tgtLocal, cg, handledMethods, uses);
            }
        }
    }

}
