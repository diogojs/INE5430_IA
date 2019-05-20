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
        self.parent: MineState = parent
        self.children = []
        self.actions = []

    def expand(self):
        """ Expande o nó gerando os nós filhos """
        if self.robot.battery == 0:
            return []

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
            child_state.try_get_gold()
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
            child_state.try_get_gold()
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
            child_state.try_get_gold()
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
            child_state.try_get_gold()
            return child_state
        else:
            return None

    def try_get_gold(self):
        x = self.robot.x()
        y = self.robot.y()
        if self.world.cell(x, y) == '*':
            self.get_gold(x, y)

    def get_gold(self, x, y):
        self.world.set_cell(x, y, 0)
        self.gold += 1
        self.actions.append('PO')

    def buy_batteries(self):
        max_need = self.world.size**2 * 2
        value = 5 * int(self.world.size**1.5)

        needed = ceil((max_need - self.robot.battery) / value)

        buy = min(needed, self.gold)
        self.robot.buy_batteries(buy * value)
        self.gold -= buy

    def zero(self):
        self.actions = []
        self.children = []
        self.parent = None
        self.cost = 0

    def __eq__(self, other):
        if not isinstance(other, MineState):
            return False
        r = self.robot
        other_r = other.robot
        w = self.world
        other_w = other.world
        return (
            r.pos == other_r.pos and
            r.battery == other_r.battery and
            r.max_battery == other_r.max_battery and
            w.matrix == other_w.matrix and
            self.cost == other.cost and
            self.gold == other.gold
        )

    def __hash__(self):
        r = self.robot
        return hash(tuple(sorted(
            [r.x(), r.y(),
             r.battery, r.max_battery,
            self.cost, self.gold]
        )))

    def __lt__(self, other):
        return (self.cost + self.h()) < (other.cost + other.h())

    def h(self):
        if self.parent is not None:
            if self.gold > self.parent.gold:
                return 0
        _h = 999
        pos = self.robot.pos
        for gold in self.world.gold_positions:
            x = abs(pos[0] - gold[0])
            y = abs(pos[1] - gold[1])
            if (x + y) < _h:
                _h = x + y
        return _h

    def isin(self, lista):
        for item in lista:
            if self.soft_equal(item):
                return True
        return False

    def soft_equal(self, other):
        r = self.robot
        other_r = other.robot
        w = self.world
        other_w = other.world
        return (
            r.pos == other_r.pos and
            r.max_battery == other_r.max_battery and
            w.matrix == other_w.matrix and
            self.gold == other.gold
        )

    def get_equal(self, lista):
        for i, item in enumerate(lista):
            if self.soft_equal(item):
                return (i, item)
        return None