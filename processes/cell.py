from enum import Enum


class CellState(Enum):
    EMPTY = 1
    BURING = 2
    LOW_VEG = 3
    MED_VEG = 4
    HIGH_VEG = 5


class Cell:

    def __init__(self, x: int, y: int, state: CellState) -> None:
        """
        Creates a cell placed at (x,y) with a state
        """
        self.x = x
        self.y = y
        self.state = state
