from heapq import heappush, heappop, heapreplace
from enum import Enum, auto
from copy import deepcopy

from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.utils.actions import reverse_actions

from miner.utils.debug import log


class InformedAgent():
    algorithms = ['astar', 'improvedastar']

    def __init__(self, alg, debugging=False):
        if alg not in InformedAgent.algorithms:
            raise ValueError(f'Algorithm {alg} not implemented')
        self.alg = alg
        self.actions = []
        self.debugging = debugging

    def search(self, initial_state: MineState, limit=0):
        self.collected_gold = 0
        self.nodes_expanded = 0
        self.initial_gold = len(initial_state.world.calc_gold_positions())
        self.best_state = initial_state

        if self.alg == 'astar':
            return self.run_AStar(initial_state)
        if self.alg == 'improvedastar':
            return self.run_improved_AStar(initial_state)

    def AStar(self, initial_state: MineState, test_function):
        """ A* search """

        frontier = []
        frontier.append(initial_state)
        explored = set()

        while len(frontier) > 0:
            state: MineState = heappop(frontier)
            explored.add(state)

            if test_function(state):
                return state

            if state.robot.battery <= 0:
                continue

            children = state.expand()
            self.nodes_expanded += len(children)

            for neighbor in children:
                isin = neighbor.isin(frontier)
                if (neighbor not in frontier) and (neighbor not in explored) and (not isin):
                    heappush(frontier, neighbor)
                elif (neighbor not in frontier) and isin:
                    self.update(frontier, neighbor)
        return None
    
    def run_AStar(self, initial_state: MineState):
        self.best_state = self.AStar(initial_state, self.test_goal_Astar)
        if self.best_state:
            self.actions = self.best_state.actions
            self.collected_gold = self.best_state.gold
        return (self, self.best_state)
    
    def run_improved_AStar(self, initial_state: MineState):
        while self.best_state.robot.battery > 1 and self.best_state.world.has_gold():
            # Procura ouro mais próximo
            initial_state = self.best_state
            initial_state.zero()
            firstgold = self.search_closest(initial_state)
            if firstgold is None:
                return (self, self.best_state)
            
            # Logging
            log(self.debugging, f'\nWent:')
            if self.debugging:
                firstgold.robot.show()
            log(self.debugging, f'Ouro: {firstgold.gold}')
            log(self.debugging, f'Bateria: {firstgold.robot.battery}')
            log(self.debugging, f'{firstgold.actions}')

            # Procura próximos ouros, até que a bateria seja no mínimo metade
            best_option = deepcopy(firstgold)
            while True:
                best_option.parent = None
                agold = self.search_closest(best_option)
                if agold is None:
                    break
                if agold.robot.battery <= agold.robot.max_battery // 2:
                    break
                best_option = agold
            # Logging
            log(self.debugging, f'\nWent:')
            if self.debugging:
                best_option.robot.show()
            log(self.debugging, f'Ouro: {best_option.gold}')
            log(self.debugging, f'Bateria: {best_option.robot.battery}')
            log(self.debugging, f'{best_option.actions}')

            # Calcula volta até a entrada
            self.best_state = best_option
            self.actions += best_option.actions
            self.actions += reverse_actions(best_option.actions)
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
        self.collected_gold = self.initial_gold - len(w.gold_positions)

        return (self, self.best_state)

    def test_goal_Astar(self, state: MineState):
        return state.robot.pos == (0, 0) and not state.world.has_gold()

    def test_goal_improved(self, state: MineState):
        if state.parent is not None:
            return state.gold > state.parent.gold
        return False
    
    def update(self, frontier, updated_state: MineState):
        i, old = updated_state.get_equal(frontier)
        if updated_state.h() < old.h():
            frontier[i] = updated_state

    def search_closest(self, start_state):
        return self.AStar(start_state, self.test_goal_improved)


if __name__ == '__main__':
    from miner.model.world import load_world
    w = load_world('./tests/example.map')
    r = Robot(w)
    ag = InformedAgent('improvedastar')
    solution, state = ag.search(MineState(r))
    if state:
        print(f'Resultado final:')
        state.robot.show()
        print(f'Nós expandidos: {solution.nodes_expanded}')
        print(f'Bateria Restante: {state.robot.battery}')
        print(f'Ouro Restante: {state.gold}')
        print(f'Ouro Total Coletado: {solution.collected_gold}')
        print(f'{solution.actions}')
    else:
        print('Nenhuma solução encontrada para esse experimento.')