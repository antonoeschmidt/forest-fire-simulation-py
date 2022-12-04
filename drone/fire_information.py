from drone.fire_coordinate import Coordinate
from typing import Tuple

class FireInformation(object):
    """Information holder for fires
    """

    def __init__(self, location: Coordinate, point: Coordinate):
        self.location = location
        self.p = point

    def __eq__(self, other):
        if isinstance(other, FireInformation):
            return self.fire == other.fire and self.location == other.location
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    
    def __gt__(self, other):
        
        p1 = self.location
        p2 = other.location
        
        return p1.distance(self.p) > p2.distance(self.p)

    def __lt__(self, other):
        return not self.__gt__(other)
