import math


class Coordinate(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def distance(self, other):
        if isinstance(other, Coordinate):
            return math.sqrt(abs(self.x - other.x) ** 2 + abs(self.y - other.y) ** 2)
        raise ValueError('Other is not of expected type')
