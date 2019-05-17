from miner.model.world import load_world
from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.agents.informed_agent import InformedAgent


def test_AStar_find(mapa='tests/mini.map'):
    algorithm = 'astar'

    # Inicializa os agentes
    world = load_world(mapa)
    robot = Robot(world)
    agent = InformedAgent(algorithm)

    print(f'Estado inicial:')
    robot.show()
    print(f'Bateria: {robot.max_battery}\n')

    solution, nodes, actions = agent.search(MineState(robot))
    if solution:
        print(f'Resultado final:')
        solution.robot.show()
        print(f'Bateria: {solution.robot.battery}')
        print(f'Nós expandidos: {nodes}')
        print(f'Ouro: {solution.gold}')
        print(f'{actions}\n')
    else:
        print('Nenhuma solução encontrada para esse experimento.')

    return solution


if __name__ == '__main__':
    mapa = "tests/mini.map"
    found = test_AStar_find(mapa)
    assert (not found.world.has_gold()), "Não encontrou todos os ouros"
    print('Teste 1: OK\n')

    mapa = "tests/impossible.map"
    found = test_AStar_find(mapa)
    assert found is None, "Encontrou quando não devia"
    print('Teste 2: OK\n')

    mapa = "tests/example.map"
    found = test_AStar_find(mapa)
    assert (not found.world.has_gold()), "Não encontrou todos os ouros"
    print('Teste 2: OK\n')
