from miner.model.world import World
from miner.utils.enums import Action

class Robot(object):

    def __init__(self, world: World, algorithm='LDS', position=(0,0)):
        if not (world and algorithm):
            raise ValueError("Parameters must not be null.")
        self.pos = position
        self.battery = 0
        self.world = world
        self.battery = int(world.size**1.5)
        self.algorithm = algorithm

    def x(self):
        return self.pos[0]
    
    def y(self):
        return self.pos[1]

    def show(self):
        self.world.show(self.pos)

    def left(self):
        return self.move(Action.LEFT, 0) is not None

    def right(self):
        return self.move(Action.RIGHT, 0) is not None

    def up(self):
        return self.move(0, Action.UP) is not None

    def down(self):
        return self.move(0, Action.DOWN) is not None

    def move(self, dx, dy):
        x = self.x()
        y = self.y()

        # Checa se está em uma borda ou de encontro a parede
        targetx = x + dx
        if targetx < 0 \
            or targetx >= self.world.size \
            or self.world.cell(targetx, y) == 1:
                return None
        targety = y + dy
        if targety < 0 \
            or targety >= self.world.size \
            or self.world.cell(x, targety) == 1:
                return None

        # Atualiza a posição e gasta bateria
        self.pos = (targetx, targety)
        self.spend_battery()
        return self.pos

    def spend_battery(self, qt=1):
        self.battery -= qt
        if self.battery < 0:
            self.battery = 0