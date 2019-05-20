from enum import IntEnum, Enum


class Action(IntEnum):
    E = -1
    D = 1
    C = -1
    B = 1
    PO = 42
    LEFT = -1
    RIGHT = 1
    UP = -1
    DOWN = 1
    GG = 42


class Algorithm(Enum):
    BFS = 'BFS'
    LDS = 'LDS'
    Astar = 'Astar'