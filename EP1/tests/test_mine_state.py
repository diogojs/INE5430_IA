from miner.model.world import World
from miner.agents.robot import Robot
from miner.model.mine_state import MineState


def test_heurisctIsLess():
    world = World(3, [0, 0, 0, 0, 1, 0, 0, '*', 0])
    robot1 = Robot(world)
    st1 = MineState(robot1)

    robot2 = Robot(world)
    robot2.pos = (1, 1)
    st2 = MineState(robot2)

    assert st2 < st1, "st2 > st1"
    assert not st2 > st1, "st2 > st1"
    assert not st2 == st1, "st2 == st1"


if __name__ == '__main__':
    test_heurisctIsLess()
