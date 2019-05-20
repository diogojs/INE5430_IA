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
        self.collected_gold = 0
        self.initial_gold = len(initial_state.world.calc_gold_positions())
        self.best_state = initial_state

        if self.alg == 'lds':
            return self.run_LDS(initial_state, limit)
        elif self.alg == 'bfs':
            return self.run_BFS(initial_state, limit)

    def run_LDS(self, initial_state: MineState, limit=0):
        while self.best_state.robot.battery > 1:
            initial_state = self.best_state
            initial_state.zero()

            # Calcula ida até o primeiro ouro
            go = self.LDS(
                initial_state, limit)
            if go is None:
                break
            # Verifica se é possível voltar até a entrada com a bateria restante
            if (go.robot.max_battery - go.robot.battery > go.robot.battery):
                break

            # Logging
            log(self.debugging, f'\nWent:')
            if self.debugging:
                go.robot.show()
            log(self.debugging, f'Ouro: {go.gold}')
            log(self.debugging, f'Bateria: {go.robot.battery}')
            log(self.debugging, f'{go.actions}')

            # Calcula volta até a entrada
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

            # Se ainda houver ouro no mapa compra bateria para a próxima busca
            if self.best_state.world.has_gold():
                self.best_state.buy_batteries()
                log(self.debugging, f'Bought: {self.best_state.robot.battery}')

        w = self.best_state.world
        if w.has_gold():
            self.collected_gold = self.initial_gold - len(w.gold_positions)
        else:
            self.collected_gold = self.initial_gold

        return (self, self.best_state)

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
        return False

    def run_BFS(self, initial_state: MineState, limit=0):
        self.best_state = self.BFS(initial_state, limit)
        if self.best_state is not None:
            self.actions = self.best_state.actions
            self.collected_gold = self.best_state.gold
        return (self, self.best_state)

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
