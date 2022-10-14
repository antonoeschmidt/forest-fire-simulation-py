from enum import Enum
from abc import ABC, abstractclassmethod


class CellState(Enum):
    EMPTY = 1
    BURNING = 2
    LOW_VEG = 3
    MED_VEG = 4
    HIGH_VEG = 5


def cell_state_description():
    """
    Prints the Label and Value for each member in the Enum
    """
    for name, value in CellState.__members__.items():
        print(f"{name}: {value.value}", end='; ')
    print()


class CellularAutomaton(ABC):
    """
    Class representing a forest as a grid and
    """

    def __init__(self, n: int, m: int):
        """

        """
        self.rows = n
        self.cols = m
        self._done = False
        self._changed = False
        self._step = 0

        self.grid = [CellState.MED_VEG for x in range(
            0, self.rows * self.cols)]

    def ignite(self, x: int, y: int):
        self.grid[self.cols * x + y] = CellState.BURNING

    def get(self, x: int, y: int) -> CellState:
        if x < 0 or x > self.rows-1:
            return CellState.EMPTY
        if y < 0 or y > self.cols-1:
            return CellState.EMPTY

        index = x * self.cols + y
        return self.grid[index]

    def _get(self, i: int) -> CellState:
        if i < 0 or i > ((self.cols * self.rows) - 1):
            return CellState.EMPTY
        return self.grid[i]

    def print(self):
        for row in range(0, self.rows):
            for cols in range(0, self.cols):
                print(f"{self._get(self.cols *row + cols).value} ", end='')
            print()
        print()

    def data(self):
        data = []
        for row in range(0, self.rows):
            rowrow = []
            for cols in range(0, self.cols):
                rowrow.append(self._get(self.cols * row + cols).value)
            data.append(rowrow)
        return data

    def step(self):
        self._changed = False
        self._step = self._step + 1
        new_grid = [self.rule(self.xy(i)) for i, c in enumerate(self.grid)]
        self.grid = new_grid

        self._done = not self._changed

    def run(self, do_print: bool):
        while not self._done:
            if do_print:
                self.print()
            self.step()

        print(f"Finished in {self._step} steps")

    def xy(self, index: int) -> tuple[int, int]:
        """
        Convert index to (x,y) coordinate
        """
        col = index % self.cols
        row = int(index / self.cols)
        return col, row

    def done(self):
        return self._done

    @abstractclassmethod
    def rule(cls, xy):
        """
        OVerride
        """
        pass
