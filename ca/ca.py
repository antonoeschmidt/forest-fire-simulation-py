from enum import Enum


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


class CellularAutomaton(object):
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

        self.grid = [CellState.MED_VEG for x in range(0, self.rows * self.cols)]

    def ignite(self, x: int, y: int):
        self.grid[self.cols * x + y] = CellState.BURNING

    def get(self, r: int, c: int):
        index = r * self.cols + c
        if index < 0 or index > (self.cols * self.rows):
            return CellState.EMPTY
        return self.grid[index]

    def _get(self, i: int):
        if i < 0 or i > ((self.cols * self.rows) - 1):
            return CellState.EMPTY
        return self.grid[i]

    def print(self):
        for row in range(0, self.rows):
            for cols in range(0, self.cols):
                print(f"{self.get(row, cols).value} ", end='')
            print()
        print()

    def step(self):
        self._changed = False
        self._step = self._step + 1
        new_grid = [self.rule(i) for i, c in enumerate(self.grid)]
        self.grid = new_grid

        self._done = not self._changed

    def run(self, do_print: bool):
        while not self._done:
            if do_print:
                self.print()
            self.step()

        print(f"Finished in {self._step} steps")

    def rule(self, index: int):
        """
        The `rule` function determines what the next state of a cell should be.

        The decision can be based on:
        * Neighbouring states
        * Wind
        * Dryness/wetness
        * And many more
        """
        # Let's make it burn for one round if N, S, E or W cell are burning
        original = self._get(index)
        new = original

        if original == CellState.BURNING or original == CellState.EMPTY:
            new = CellState.EMPTY

        elif CellState.BURNING in [self._get(x) for x in [index - 1, index + 1, index + self.rows, index - self.rows]]:
            new = CellState.BURNING

        self._changed |= new != original
        return new
