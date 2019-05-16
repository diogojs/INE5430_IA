from collections import deque
from enum import Enum, auto

from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from utils.actions import reverse_actions


class UninformedAgent():
    algorithms = ['LDS', 'Astar']

    def __init__(self, alg):
        if alg not in UninformedAgent.algorithms:
            raise ValueError(f'Algorithm {alg} not implemented')
        self.alg = alg
        self.actions = []

    def search(self, initial_state: MineState, limit=0):

        self.nodes_expanded = 0
        self.best_state = initial_state

        if self.alg == 'LDS':
            while self.best_state.robot.battery > 1:
                # Verifica ida mais eficiente do robô
                initial_state = self.best_state
                initial_state.zero()

                go = self.LDS(
                    initial_state, self.test_going, limit)
                if go is None:
                    break

                print(f'\nWent:')
                go.robot.show()
                print(f'Ouro: {go.gold}')
                print(f'Bateria: {go.robot.battery}')
                print(f'{go.actions}')

                self.best_state = go
                self.actions += go.actions
                self.actions += reverse_actions(go.actions)
                self.best_state.robot.pos = (0, 0)
                self.best_state.robot.battery = 2 * \
                    self.best_state.robot.battery - self.best_state.robot.max_battery

                print(f'\nBack:')
                self.best_state.robot.show()
                print(f'Bateria: {self.best_state.robot.battery}')
                print(f'{self.actions}')

                if self.best_state.world.has_gold():
                    self.best_state.buy_batteries()
                    print(f'Bought: {self.best_state.robot.battery}')

            return (self.best_state, self.nodes_expanded, self.actions)

    def LDS(self, initial_state: MineState, test_function, limit=0) -> (MineState, int):
        """ Limited Depth Search """

        if limit == 0:
            self.limit = initial_state.robot.battery // 2
            print(f'Setting depth limit to {self.limit}')
        else:
            self.limit = limit

        frontier = deque()
        frontier.append(initial_state)
        explored = set()

        while len(frontier) > 0:
            state: MineState = frontier.pop()
            explored.add(state)

            if test_function(state):
                state.get_gold()
                return state

            if state.cost >= limit:
                continue

            children = state.expand()
            self.nodes_expanded += len(children)

            for neighbor in children:
                if (neighbor not in frontier) and (neighbor not in explored):
                    frontier.append(neighbor)

        return None

    def test_going(self, state: MineState):
        r = state.robot
        return state.world.cell(r.x(), r.y()) == '*'

    def test_back(self, state: MineState):
        return state.robot.pos == (0, 0)
