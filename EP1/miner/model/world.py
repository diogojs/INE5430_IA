"""
    Guarda a configuração do mundo/mina
"""

class World(object):
    
    def __init__(self, size: int, matrix: []):
        if size*size != len(matrix) or size < 2:
            raise Exception("The lenght of matrix is not correct!")
        self.size = size
        self.matrix = matrix

    def cell(self, x, y) -> int:
        return self.matrix[y*self.size + x]

    def get(self, index) -> (int, int):
        return (index % self.size, index // self.size)

    def view(self, x, y):
        c = self.cell(x, y)
        if c == '0':
            return ' '
        elif c == '1':
            return ':'
        else:
            return '*'

    def show(self, robot_position=(0,0)):
        for y in range(self.size):
            line = ''
            for x in range(self.size):
                if (robot_position == (x,y)):
                    if self.cell(x, y) == '*':
                        line += '$ '
                    else:
                        line += '@ '
                else:
                    line += self.cell(x, y) + ' '
            print(line)