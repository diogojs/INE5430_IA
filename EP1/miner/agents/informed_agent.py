from heapq import heappush, heappop
from enum import Enum, auto

from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.utils.actions import reverse_actions

from miner.utils.debug import log


class InformedAgent():
    algorithms = ['astar']

    def __init__(self, alg, debugging=False):
        if alg not in InformedAgent.algorithms:
            raise ValueError(f'Algorithm {alg} not implemented')
        self.alg = alg
        self.actions = []
        self.debugging = debugging

    def search(self, initial_state: MineState, limit=0):

        self.nodes_expanded = 0
        self.best_state = initial_state

        if self.alg == 'astar':
            return self.run_AStar(initial_state)

    def run_AStar(self, initial_state: MineState):
        self.best_state = self.AStar(initial_state)
        if self.best_state:
            self.actions = self.best_state.actions
        return (self.best_state, self.nodes_expanded, self.actions)

    def AStar(self, initial_state: MineState):
        """ A* search """

        frontier = []
        frontier.append(initial_state)
        explored = set()

        while len(frontier) > 0:
            state: MineState = heappop(frontier)
            explored.add(state)

            if self.test_goal_Astar(state):
                return state

            if state.robot.battery <= 0:
                continue

            children = state.expand()
            self.nodes_expanded += len(children)

            for neighbor in children:
                if (neighbor not in frontier) and (neighbor not in explored):
                    heappush(frontier, neighbor)
                elif (neighbor in frontier):
                    self.update(frontier, neighbor)
        return None

    def test_goal_Astar(self, state: MineState):
        return state.robot.pos == (0, 0) and not state.world.has_gold()

    def update(self, frontier, updated_state):
        pass
