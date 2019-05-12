from collections import deque
from enum import Enum, auto

class Algorithm(Enum):
    LDS = 'LDS'
    Astar = 'Astar'


def LDS(initial_state):
    """LDS search"""
    frontier = deque()
    frontier.append(initial_state)
    explored = set()

    nodes_expanded = 0

    while len(frontier) > 0:
        state = frontier.popleft()
        explored.add(state)

        if test_goal(state):
            return (state, nodes_expanded)

        children = state.expand()
        nodes_expanded += len(children)
        loop_part(children, frontier, explored)
    return (None, 0, 0)
