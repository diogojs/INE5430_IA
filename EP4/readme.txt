Para rodar o sistema de estacionamento do caminhão, basta seguir os passos abaixo:

Na pasta geral “Logica_Fuzzy_Diogo_Jacyara” rodar o server.jar em um terminal

			java -jar server.jar 

Com outro terminal aberto na mesma pasta, rodar o remoteDriver.jar

java -jar remoteDriver.jar

	Para gerar os conjuntos fuzzy através da biblioteca jFuzzyLogic, basta rodar o jFuzzyLogic.jar passando com o parâmetro do arquivo “truck.fcl” onde estão as regras, entradas e saídas, conforme a seguir:
	
Na pasta geral “Logica_Fuzzy_Diogo_Jacyara” rodar o seguinte comando

java -jar jFuzzyLogic.jar truck.fcl

