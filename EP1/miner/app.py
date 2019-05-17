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
    # Salva argumentos da linha de comando
    if len(sys.argv) < 2:
        print('Argumentos inválidos.')
        print('Informe o algoritmo a ser utilizado, e o limite caso necessário.')
        print('Exemplo de entrada: python app.py LDS 20')
        exit()
    algorithm = sys.argv[1].lower()

    limit = 0
    if len(sys.argv) > 2 and sys.argv[2].lower() != 'debug':
        limit = int(sys.argv[2].lower())

    debugging = False
    if 'debug' in sys.argv:
        debugging = True

    # Inicializa os agentes
    world = load_world(
        '/home/diogo/Documents/CCO/2019-1/INE5430_IA/EP1/tests/example.map')
    robot = Robot(world)
    agent = UninformedAgent('LDS', debugging)
    print(f'Estado inicial:')
    robot.show()
    print(f'Bateria disponível: {robot.max_battery}')
    print('\nIniciando busca...\n')

    solution, nodes, actions = agent.search(
        MineState(robot), limit)
    if solution:
        print(f'Resultado final:')
        solution.robot.show()
        print(f'Nós expandidos: {nodes}')
        print(f'Ouro: {solution.gold}')
        print(f'Bateria: {solution.robot.battery}')
        print(f'{actions}')
    else:
        print('Nenhuma solução encontrada para esse experimento.')
