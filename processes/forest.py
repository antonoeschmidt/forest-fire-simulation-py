from ca.simplefire import SimpleCa

class Forest(object):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.fire = SimpleCa(width, height)
        self.fire.ignite(3,3)

    def step(self):
        self.fire.step()

    def get_data(self):
        return self.fire.data()

    # def get_cell(self, x, y):
    #     return self.map[x * self.width + y]
