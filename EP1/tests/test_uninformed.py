from miner.model.world import load_world
from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.agents.uninformed_agent import UninformedAgent


def test_LDS_find(mapa='tests/mini.map', limit=0):
    algorithm = 'lds'

    # Inicializa os agentes
    world = load_world(mapa)
    robot = Robot(world)
    agent = UninformedAgent(algorithm)

    _, state = agent.search(
        MineState(robot), limit)
    return state


if __name__ == '__main__':
    mapa = "tests/mini.map"
    found = test_LDS_find(mapa, 4)
    assert len(found.world.gold_positions) == 1, "Não pegou 1 ouro"
    print('Teste 1: OK')
    found = test_LDS_find(mapa, 20)
    assert (not found.world.has_gold()), "Não pegou todos os ouros"
    print('Teste 2: OK')

    mapa = "tests/example.map"
    found = test_LDS_find(mapa, 8)
    assert len(
        found.world.gold_positions) == 4, "Encontrou ouro quando não devia encontrar"
    print('Teste 3: OK')
    found = test_LDS_find(mapa, 16)
    assert len(
        found.world.gold_positions) == 2, "Encontrou um numero diferente de 2 ouros"
    print('Teste 4: OK')

    found = test_LDS_find(mapa, 20)
    assert (not found.world.has_gold()), "Não pegou todos os ouros"
    print('Teste 5: OK')
