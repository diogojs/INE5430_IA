from copy import deepcopy
from math import ceil

from miner.agents.robot import Robot


class MineState():
    """
        Representa um nó-estado do problema
    """

    def __init__(self, robot: Robot, parent=None, cost=0, gold=0):
        self.robot = robot
        self.world = robot.world
        self.cost = cost
        self.gold = gold
        self.parent = parent
        self.children = []
        self.actions = []

    def expand(self):
        """ Expande o nó gerando os nós filhos """
        if self.robot.battery == 0:
            return self.children

        if len(self.children) == 0:
            ac = (len(self.actions) == 0)
            if ac or self.actions[-1] != 'B':
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
            if ac or self.actions[-1] != 'C':
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
            if ac or self.actions[-1] != 'D':
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
            if ac or self.actions[-1] != 'E':
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
        return self.children

    def move_up(self):
        pos = self.robot.up()
        if pos is not None:
            child_robot = deepcopy(self.robot)
            child_robot.pos = pos
            child_robot.spend_battery()
            child_state = MineState(child_robot, self, self.cost+1, self.gold)
            child_state.actions = list(self.actions)
            child_state.actions.append('C')
            return child_state
        else:
            return None

    def move_down(self):
        pos = self.robot.down()
        if pos is not None:
            child_robot = deepcopy(self.robot)
            child_robot.pos = pos
            child_robot.spend_battery()
            child_state = MineState(child_robot, self, self.cost+1, self.gold)
            child_state.actions = list(self.actions)
            child_state.actions.append('B')
            return child_state
        else:
            return None

    def move_left(self):
        pos = self.robot.left()
        if pos is not None:
            child_robot = deepcopy(self.robot)
            child_robot.pos = pos
            child_robot.spend_battery()
            child_state = MineState(child_robot, self, self.cost+1, self.gold)
            child_state.actions = list(self.actions)
            child_state.actions.append('E')
            return child_state
        else:
            return None

    def move_right(self):
        pos = self.robot.right()
        if pos is not None:
            child_robot = deepcopy(self.robot)
            child_robot.pos = pos
            child_robot.spend_battery()
            child_state = MineState(child_robot, self, self.cost+1, self.gold)
            child_state.actions = list(self.actions)
            child_state.actions.append('D')
            return child_state
        else:
            return None

    def try_get_gold(self):
        x = self.robot.x()
        y = self.robot.y()
        if self.world.cell(x, y) == '*':
            self.world.set_cell(x, y, 0)
            self.gold += 1

    def get_gold(self):
        self.gold += 1
        x = self.robot.x()
        y = self.robot.y()
        self.world.set_cell(x, y, 0)

    def buy_batteries(self):
        max_need = self.world.size**2 * 2
        value = 5 * int(self.world.size**1.5)

        if self.robot.battery < max_need:
            self.robot.buy_batteries(self.gold)
            self.gold = 0

    def zero(self):
        self.actions = []
        self.children = []
        self.parent = None
        self.cost = 0
