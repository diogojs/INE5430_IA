from miner.model.world import load_world, World
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

    solution, state = agent.search(
        MineState(robot))
    if state:
        print(f'Resultado final:')
        state.robot.show()
        print(f'Nós expandidos: {solution.nodes_expanded}')
        print(f'Bateria Restante: {state.robot.battery}')
        print(f'Ouro Restante: {state.gold}')
        print(f'Ouro Total Coletado: {solution.collected_gold}')
        print(f'{solution.actions}')
    else:
        print('Nenhuma solução encontrada para esse experimento.')

    return state

def test_improvedAStar(mapa='tests/mini.map'):
    algorithm = 'improvedastar'

    # Inicializa os agentes
    world = load_world(mapa)
    robot = Robot(world)
    agent = InformedAgent(algorithm)

    print(f'Estado inicial:')
    robot.show()
    print(f'Bateria: {robot.max_battery}\n')

    solution, state = agent.search(
        MineState(robot))
    if state:
        print(f'Resultado final:')
        state.robot.show()
        print(f'Nós expandidos: {solution.nodes_expanded}')
        print(f'Bateria Restante: {state.robot.battery}')
        print(f'Ouro Restante: {state.gold}')
        print(f'Ouro Total Coletado: {solution.collected_gold}')
        print(f'{solution.actions}')
    else:
        print('Nenhuma solução encontrada para esse experimento.')

    return state

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
    assert (not found), "Não encontrou todos os ouros"
    print('Teste 3: OK\n')

    mapa = "tests/example.map"
    found = test_improvedAStar(mapa)
    assert (not found.world.has_gold()), "Não encontrou todos os ouros"
    print('Teste 4: OK\n')
