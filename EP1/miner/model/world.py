"""
    Guarda a configuração do mundo/mina
"""


def load_world(filepath):
    f = open(filepath, 'r')
    if f == None:
        raise FileNotFoundError

    try:
        size = int(f.read(1))
    except ValueError:
        print('Invalid file format.')
        return

    matrix = []
    for line in f:
        for item in line:
            if item == '0':
                matrix.append(0)
            elif item == '1':
                matrix.append(1)
            elif item == '*':
                matrix.append('*')
    return World(size, matrix)


class World(object):

    def __init__(self, size: int, matrix: []):
        if size*size != len(matrix) or size < 2:
            raise Exception("The lenght of matrix is not correct!")
        self.size = size
        self.matrix = matrix

    def cell(self, x, y) -> int:
        return self.matrix[y*self.size + x]

    def set_cell(self, x, y, value):
        self.matrix[y*self.size + x] = value

    def get(self, index) -> (int, int):
        return (index % self.size, index // self.size)

    def view(self, x, y):
        c = self.cell(x, y)
        if c == 0:
            return ' '
        elif c == 1:
            return ':'
        else:
            return '*'

    def show(self, robot_position=(0, 0)):
        for y in range(self.size):
            line = ''
            for x in range(self.size):
                if (robot_position == (x, y)):
                    if self.cell(x, y) == '*':
                        line += '$ '
                    else:
                        line += '@ '
                else:
                    line += str(self.cell(x, y)) + ' '
            print(line)

    def has_gold(self):
        return '*' in self.matrix
