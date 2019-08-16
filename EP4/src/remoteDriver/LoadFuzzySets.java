package remoteDriver;

import net.sourceforge.jFuzzyLogic.FIS;
import net.sourceforge.jFuzzyLogic.rule.Rule;

public class LoadFuzzySets {
	private static String FILEPATH = "./truck.fcl";
	private static String ANGLE_NAME = "angle";
	private static String XPOSITION_NAME = "xposition";
	private static String DIRECTION_NAME = "direction";

	FIS fis;

	public void load() {
		this.fis = FIS.load(FILEPATH, true);
	}

	public double direction(double angle, double xposition) {
		this.fis.setVariable(ANGLE_NAME, angle); 
		this.fis.setVariable(XPOSITION_NAME, xposition);
		this.fis.evaluate();
		double directionValue = this.fis.getVariable(DIRECTION_NAME).getValue();
		 for( Rule r : fis.getFunctionBlock("truckPark").getFuzzyRuleBlock("No1").getRules() )
		      System.out.println(r);
		 return directionValue;
	}

}
