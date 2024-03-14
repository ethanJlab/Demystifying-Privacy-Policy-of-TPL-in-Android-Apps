package moon;

import soot.Body;
import soot.Local;
import soot.Unit;
import soot.jimple.Stmt;
import soot.toolkits.graph.BriefUnitGraph;
import soot.toolkits.graph.UnitGraph;
import soot.toolkits.scalar.SimpleLocalDefs;
import soot.toolkits.scalar.SimpleLocalUses;
import soot.toolkits.scalar.UnitValueBoxPair;

import java.util.*;

// local variable analysis
public class IntraProcedureVariableAnalysis {
	
	// ---- //
	
	public static List<Unit> findDefs(Body body, Stmt stmt, Local local) {
		UnitGraph cfg = new BriefUnitGraph(body);
		SimpleLocalDefs defsResolver = new SimpleLocalDefs(cfg);
		List<Unit> defs = defsResolver.getDefsOfAt(local, stmt);
		
		return defs;
	}
	
	// ---- //
	
	public static List<UnitValueBoxPair> findUses(Body body, Stmt stmt, Local local) {
		UnitGraph cfg = new BriefUnitGraph(body);
		SimpleLocalDefs defsResolver = new SimpleLocalDefs(cfg);
		List<Unit> defs = defsResolver.getDefsOfAt(local, stmt);
		SimpleLocalUses usesResolver = new SimpleLocalUses(cfg, defsResolver);
		List<UnitValueBoxPair> uses = new ArrayList<UnitValueBoxPair>();
		for (Unit def : defs) {
			List<UnitValueBoxPair> pairs = usesResolver.getUsesOf(def);
			uses.addAll(pairs);
		}
		
		return uses;
	}
	
	public static List<UnitValueBoxPair> findUsesBckward(Body body, Stmt stmt, Local local) {
		// collect units executed before the input "stmt"
		UnitGraph cfg = new BriefUnitGraph(body);
		HashSet<Unit> preUnits = new HashSet<Unit>();
		Queue<Unit> queue = new LinkedList<Unit>();
		queue.addAll(cfg.getPredsOf(stmt)); // <- 
		while (!queue.isEmpty()) {
			Unit curUnit = queue.poll();
			if (preUnits.contains(curUnit))
				continue;
			preUnits.add(curUnit);
			for (Unit preUnit : cfg.getPredsOf(curUnit))
				if (!preUnits.contains(preUnit) && !queue.contains(preUnit))
					queue.add(preUnit);
		}
		// filter out excluded uses
		List<UnitValueBoxPair> output = new ArrayList<UnitValueBoxPair>();
		List<UnitValueBoxPair> uses = findUses(body, stmt, local); // inaccurate uses
		for (UnitValueBoxPair use : uses) 
			if (preUnits.contains(use.unit))
				output.add(use);
		
		return output;
	}
	
	public static List<UnitValueBoxPair> findUsesForward(Body body, Stmt stmt, Local local) {
		// collect units executed after the input "stmt"
		UnitGraph cfg = new BriefUnitGraph(body);
		HashSet<Unit> pstUnits = new HashSet<Unit>();
		Queue<Unit> queue = new LinkedList<Unit>();
		queue.addAll(cfg.getSuccsOf(stmt)); // <- 
		while (!queue.isEmpty()) {
			Unit curUnit = queue.poll();
			if (pstUnits.contains(curUnit))
				continue;
			pstUnits.add(curUnit);
			for (Unit pstUnit : cfg.getSuccsOf(curUnit))
				if (!pstUnits.contains(pstUnit) && !queue.contains(pstUnit))
					queue.add(pstUnit);
		}
		// filter out excluded uses
		List<UnitValueBoxPair> output = new ArrayList<UnitValueBoxPair>();
		List<UnitValueBoxPair> uses = findUses(body, stmt, local); // inaccurate uses
		for (UnitValueBoxPair use : uses) 
			if (pstUnits.contains(use.unit))
				output.add(use);
		
		return output;
	}

}
