# Projeto desenvolvido para a disciplina INE5430
# Aluno: Diogo Junior de Souza
# Matricula: 16100721
# Semestre: 2019.1

import sys

from miner.model.world import load_world
from miner.model.mine_state import MineState
from miner.agents.robot import Robot
from miner.agents.uninformed_agent import UninformedAgent

if __name__ == "__main__":
    # Inicializa os agentes
    world = load_world('/home/diogo/Documents/CCO/07sem/INE5430_IA/EP1/tests/example.map')
    robot = Robot(world)
    agent = UninformedAgent(MineState(robot))
    agent.search('LDS', agent.best_state)
