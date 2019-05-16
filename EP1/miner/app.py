# Projeto desenvolvido para a disciplina INE5430
# Aluno: Diogo Junior de Souza
# Matricula: 16100721
# Semestre: 2019.1

import sys

from miner.model.world import load_world
from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.agents.uninformed_agent import UninformedAgent

if __name__ == "__main__":
    # Inicializa os agentes
    world = load_world(
        '/home/diogo/Documents/CCO/2019-1/INE5430_IA/EP1/tests/example.map')
    robot = Robot(world)
    agent = UninformedAgent('LDS')
    print(f'Estado inicial:')
    robot.show()
    print(f'Bateria disponível: {robot.max_battery}')

    print('\niniciando busca...\n')

    solution, nodes, actions = agent.search(
        MineState(robot), robot.max_battery)
    if solution:
        print(f'Resultado final:')
        solution.robot.show()
        print(f'Nós expandidos: {nodes}')
        print(f'Ouro: {solution.gold}')
        print(f'Bateria: {solution.robot.battery}')
        print(f'{actions}')
    else:
        print('Nenhuma solução encontrada para esse experimento.')
