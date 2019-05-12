from miner.model.world import World
from miner.agents.robot import Robot


def test_robot():
    world = World(3, ['0','0','0','1','1','0','0','*','0'])
    robot = Robot(world, 'LDS')
    robot.pos = (1, 0)
    robot.show()


if __name__ == '__main__':
    test_robot()
