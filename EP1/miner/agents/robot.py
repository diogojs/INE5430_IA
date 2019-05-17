from miner.model.world import World
from miner.utils.enums import Action


class Robot(object):

    def __init__(self, world: World, position=(0, 0)):
        if not world:
            raise ValueError("Parameter world must not be null.")
        self.pos = position
        self.battery = 0
        self.world = world
        self.max_battery = int(world.size**1.5)
        self.battery = self.max_battery

    def x(self):
        return self.pos[0]

    def y(self):
        return self.pos[1]

    def show(self):
        self.world.show(self.pos)

    def left(self):
        return self.move(Action.LEFT, 0)

    def right(self):
        return self.move(Action.RIGHT, 0)

    def up(self):
        return self.move(0, Action.UP)

    def down(self):
        return self.move(0, Action.DOWN)

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

        # Retorna a nova posição
        return (targetx, targety)

    def spend_battery(self, qt=1):
        self.battery -= qt
        if self.battery < 0:
            self.battery = 0

    def buy_batteries(self, amount):
        self.battery += amount
        self.max_battery = self.battery
