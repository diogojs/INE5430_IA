from collections import deque
from enum import Enum, auto

from miner.model.mine_state import MineState
from miner.agents.robot import Robot


class UninformedAgent():
    algorithms = ['LDS', 'Astar']

    def __init__(self, initial_state: MineState):
        self.robot = initial_state.robot
        self.world = initial_state.robot.world
        self.final_battery = self.robot.battery
        self.collected_gold = 0
        self.actions = []
        self.best_state: MineState = initial_state

    def search(self, alg, initial_state: MineState):
        if alg not in UninformedAgent.algorithms:
            raise ValueError(f'Algorithm {alg} not implemented')
        nodes_expanded = 0
        if alg == 'LDS':
            # while self.final_battery > 0:
                # Verifica ida mais eficiente do robô
                going_state, nodes_expanded = self.LDS(initial_state, self.test_going, 10)
                # back_state = self.LDS(going_state, self.test_back, 10)
                going_state.robot.show()
                print(f'Expanded: {nodes_expanded}')
                

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
        nodes_expanded = 0

        while len(frontier) > 0:
            state: MineState = frontier.pop()
            explored.add(state)
            if state.cost > limit:
                continue

            if test_function(state):
                self.best_state = state

            children = state.expand()
            nodes_expanded += len(children)
            
            for neighbor in children:
                if (neighbor not in frontier) and (neighbor not in explored):
                    frontier.append(neighbor)
        
        return (self.best_state, nodes_expanded)

    def test_going(self, state: MineState):
        state.try_get_gold()
        if state.gold >= self.best_state.gold:
            return state.gold > self.best_state.gold or state.robot.battery > self.best_state.robot.battery

    def test_back(self, state: MineState):
        pass