package remoteDriver;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.StringTokenizer;

import net.sourceforge.jFuzzyLogic.FIS;
import net.sourceforge.jFuzzyLogic.rule.Rule;

public class RemoteDriver {

	static int port = 4321;
	static String host = "localhost";

	private static String FILEPATH = "./truck.fcl";
	private static String ANGLE_NAME = "angle";
	private static String XPOSITION_NAME = "xposition";
	private static String DIRECTION_NAME = "direction";

	private static FIS fis;

	public static void main(String[] args) throws IOException {

		Socket kkSocket = null;
		PrintWriter out = null;
		BufferedReader in = null;

		try {
			kkSocket = new Socket(host, port);
			out = new PrintWriter(kkSocket.getOutputStream(), true);
			in = new BufferedReader(new InputStreamReader(kkSocket.getInputStream()));
		} catch (UnknownHostException e) {
			System.err.println("Don't know about host:" + host);
			System.exit(1);
		} catch (IOException e) {
			System.err.println("Couldn't get I/O for the connection to: " + host);
			System.exit(1);
		}

		// Inicializa os conjuntos fuzzy
		fis = FIS.load(FILEPATH, true);

		BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
		String fromServer;

		double x, y;
		double angle;

		// requisicao da posicao do caminhao
		out.println("r");
		while ((fromServer = in.readLine()) != null) {
			StringTokenizer st = new StringTokenizer(fromServer);
			x = Double.valueOf(st.nextToken()).doubleValue();
			y = Double.valueOf(st.nextToken()).doubleValue();
			angle = Double.valueOf(st.nextToken()).doubleValue();

			System.out.println("x: " + x + " y: " + y + " angle: " + angle);

			// Tomada de decisao do caminhão
			out.println(direction(angle, x));

			// requisicao da posicao do caminhao
			out.println("r");
		}

		out.close();
		in.close();
		stdIn.close();
		kkSocket.close();
	}

	private static double direction(double angle, double xposition) {
		fis.setVariable(ANGLE_NAME, angle);
		fis.setVariable(XPOSITION_NAME, xposition);
		fis.evaluate();
		double directionValue = fis.getVariable(DIRECTION_NAME).getValue();
		for (Rule r : fis.getFunctionBlock("truckPark").getFuzzyRuleBlock("No1").getRules())
			System.out.println(r);
		return normalize(directionValue);
	}

	private static normalize(double direction) {
		return direction / 30;
	}
}