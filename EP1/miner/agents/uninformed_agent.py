from collections import deque
from enum import Enum, auto

from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.utils.actions import reverse_actions

from miner.utils.debug import log


class UninformedAgent():
    algorithms = ['lds', 'bfs']

    def __init__(self, alg, debugging=False):
        if alg not in UninformedAgent.algorithms:
            raise ValueError(f'Algorithm {alg} not implemented')
        self.alg = alg
        self.actions = []
        self.debugging = debugging

    def search(self, initial_state: MineState, limit=0):

        self.nodes_expanded = 0
        self.best_state = initial_state

        if self.alg == 'lds':
            return self.run_LDS(initial_state, limit)
        elif self.alg == 'bfs':
            return self.run_BFS(initial_state, limit)

    def run_LDS(self, initial_state: MineState, limit=0):
        while self.best_state.robot.battery > 1:
            # Verifica ida mais eficiente do robô
            initial_state = self.best_state
            initial_state.zero()

            go = self.LDS(
                initial_state, limit)
            if go is None:
                break
            if (go.robot.max_battery - go.robot.battery > go.robot.battery):
                break

            # Logging
            log(self.debugging, f'\nWent:')
            if self.debugging:
                go.robot.show()
            log(self.debugging, f'Ouro: {go.gold}')
            log(self.debugging, f'Bateria: {go.robot.battery}')
            log(self.debugging, f'{go.actions}')

            self.best_state = go
            self.actions += go.actions
            self.actions += reverse_actions(go.actions)
            self.best_state.robot.pos = (0, 0)
            self.best_state.robot.battery = 2 * \
                self.best_state.robot.battery - self.best_state.robot.max_battery

            # Logging
            log(self.debugging, f'\nBack:')
            if self.debugging:
                self.best_state.robot.show()
            log(self.debugging, f'Bateria: {self.best_state.robot.battery}')
            log(self.debugging, f'{self.actions}')

            if self.best_state.world.has_gold():
                self.best_state.buy_batteries()
                log(self.debugging, f'Bought: {self.best_state.robot.battery}')

        return (self.best_state, self.nodes_expanded, self.actions)

    def LDS(self, initial_state: MineState, limit=0) -> (MineState, int):
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

            if self.test_goal_lds(state):
                return state

            if state.cost >= self.limit or state.robot.battery <= 0:
                continue

            children = state.expand()
            self.nodes_expanded += len(children)

            for neighbor in children:
                if (neighbor not in frontier) and (neighbor not in explored):
                    frontier.append(neighbor)

        return None

    def test_goal_lds(self, state: MineState):
        if state.parent is not None:
            return state.gold > state.parent.gold

    def run_BFS(self, initial_state: MineState, limit=0):
        self.best_state = self.BFS(initial_state, limit)
        self.actions = self.best_state.actions
        return (self.best_state, self.nodes_expanded, self.actions)

    def BFS(self, initial_state: MineState, limit=0):
        """ Breath First Search """

        if limit == 0:
            self.limit = initial_state.robot.battery
            print(f'Setting depth limit to {self.limit}')
        else:
            self.limit = limit

        frontier = deque()
        frontier.append(initial_state)
        explored = set()

        while len(frontier) > 0:
            state: MineState = frontier.popleft()
            explored.add(state)

            if self.test_goal_BFS(state):
                return state

            if state.cost >= limit or state.robot.battery <= 0:
                continue

            children = state.expand()
            self.nodes_expanded += len(children)

            for neighbor in children:
                if (neighbor not in frontier) and (neighbor not in explored):
                    frontier.append(neighbor)

        return None

    def test_goal_BFS(self, state: MineState):
        return state.robot.pos == (0, 0) and not state.world.has_gold()
