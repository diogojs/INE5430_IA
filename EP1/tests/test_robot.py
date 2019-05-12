from miner.model.world import World
from miner.agents.robot import Robot


def test_isInBorder_DontMove():
    world = World(3, [0,0,0,0,1,0,0,'*',0])
    robot = Robot(world, 'LDS')
    pre = (0,0)
    robot.pos = pre
    assert robot.left() == False, "Should not go left"
    assert robot.pos == pre, "Went left, should fail"
    pre = (2,0)
    robot.pos = pre
    assert robot.right() == False, "Should not go right"
    assert robot.pos == pre, "Went right, should fail"
    assert robot.up() == False, "Should not go up"
    assert robot.pos == pre, "Went up, should fail"
    pre = (2,2)
    robot.pos = pre
    assert robot.down() == False, "Should not go down"
    assert robot.pos == pre, "Went down, should fail"

def test_goToWall_DontMove():
    world = World(3, [0,0,0,0,1,0,0,'*',0])
    robot = Robot(world, 'LDS')
    pre = (2,1)
    robot.pos = pre
    assert robot.left() == False, "Should collide towall"
    assert robot.pos == pre, "Went left, should fail"
    pre = (0,1)
    robot.pos = pre
    assert robot.right() == False, "Should collid to wall"
    assert robot.pos == pre, "Went right, should fail"
    pre = (1,0)
    robot.pos = pre
    assert robot.down() == False, "Should collid to wall"
    assert robot.pos == pre, "Went down, should fail"
    pre = (1,2)
    robot.pos = pre
    assert robot.up() == False, "Should collid to wall"
    assert robot.pos == pre, "Went up, should fail"


if __name__ == '__main__':
    test_isInBorder_DontMove()
    test_goToWall_DontMove()
