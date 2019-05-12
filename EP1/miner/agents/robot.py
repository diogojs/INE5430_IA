from miner.model.world import World

class Robot(object):

    def __init__(self, world: World, algorithm: str, position=(0,0)):
        if not (world and algorithm):
            raise ValueError("Parameters must not be null.")
        self.pos = position
        self.battery = 0
        self.world = world
        self.battery = int(world.size**1.5)
        self.algorithm = algorithm

    def show(self):
        self.world.show(self.pos)