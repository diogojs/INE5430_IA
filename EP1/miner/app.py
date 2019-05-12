# Projeto desenvolvido para a disciplina INE5430
# Aluno: Diogo Junior de Souza
# Matricula: 16100721
# Semestre: 2019.1

import sys

from miner.model.world import World
from miner.agents.robot import Robot

if __name__ == "__main__":
    # Inicializa os agentes
    world = World(3, ['0','0','0','1','1','0','0','*','0'])
    robot = Robot(world, 'LDS')
    robot.pos = (1, 0)
    robot.show()
    pass