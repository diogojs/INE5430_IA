from miner.model.world import World


def test_world():
    world = World(3, ['0','0','0','1','1','0','0','*','0'])
    world.show()
    assert world.cell(0, 0) == '0'
    assert world.cell(0, 1) == '1'
    assert world.cell(1, 2) == '*'


if __name__ == '__main__':
    test_world()
