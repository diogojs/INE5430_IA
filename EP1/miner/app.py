# Projeto desenvolvido para a disciplina INE5430
# Aluno: Diogo Junior de Souza
# Matricula: 16100721
# Semestre: 2019.1

import os
import sys

from miner.model.world import load_world
from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.agents.uninformed_agent import UninformedAgent
from miner.agents.informed_agent import InformedAgent


if __name__ == "__main__":
    # Valida argumentos da linha de comando
    if len(sys.argv) < 3:
        print('Argumentos inválidos.')
        print('Informe o arquivo contendo o mapa, o algoritmo a ser utilizado')
        print('e o limite do algoritmo caso necessário.')
        print('Exemplo de entrada: python app.py ./tests/example.map LDS 20')
        print('Algoritmos implementados: LDS, BFS, Astar, ImprovedAstar')
        exit()
    mapa = sys.argv[1]
    algorithm = sys.argv[2].lower()

    if (algorithm == 'lds' or algorithm == 'bfs') and len(sys.argv) < 4:
        print('Informe o limite do algoritmo a ser utilizado.')
        print('Exemplo de entrada: python app.py ./tests/example.map LDS 20')
        exit()
    
    limit = 0
    if len(sys.argv) > 3:
        try:
            limit = int(sys.argv[3])
        except ValueError:
            pass

    debugging = False
    if 'debug' in sys.argv:
        debugging = True

    # Inicializa os agentes
    world = load_world(mapa)
    robot = Robot(world)
    if algorithm in UninformedAgent.algorithms:
        agent = UninformedAgent(algorithm, debugging)
    elif algorithm in InformedAgent.algorithms:
        agent = InformedAgent(algorithm, debugging)
    else:
        print('Algoritmo não implementado.')
        exit()

    print(f'Estado inicial:')
    robot.show()
    print(f'Bateria disponível: {robot.max_battery}')
    print(f'\nIniciando busca com {algorithm.upper()}...\n')

    solution, state = agent.search(
        MineState(robot), limit)
    print(f'Resultado final:')
    print(f'Nós expandidos: {solution.nodes_expanded}')
    if state:
        state.robot.show()
        print(f'Saldo Bateria: {state.robot.battery}')
        print(f'Saldo Ouro: {state.gold}')
        print(f'Ouro Total Coletado: {solution.collected_gold}')
        print(f'{solution.actions}\n')
    else:
        print('Nenhuma solução encontrada para esse experimento.\n')
