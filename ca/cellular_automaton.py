import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class VegetationType(Enum):
    LOW_VEG = 3
    MED_VEG = 4
    HIGH_VEG = 5
    WATER = 6
    ROCK = 7


class FrontEndValues(Enum):
    BURNED = 1
    BURNING = 2
    LOW_VEG = 3
    MED_VEG = 4
    HIGH_VEG = 5
    WATER = 6
    ROCK = 7


@dataclass(frozen=True)
class CellObject:
    """
    Veg (vegetation type): integer = matching the Enum of CellState
    Fire: integer = counts how many ticks the cell has been burning for
    Wind: Tuple(int,int) = vector determining the wind for that cell
    Hydration: float = a percentage of hydration
    """
    veg: VegetationType
    fire: int
    fire_intensity: int
    wind: Tuple[int, int]
    hydration: float
    burned: bool

    def factory(self, veg: int = None, fire: int = None, fire_intensity: float = None, wind: Tuple[int, int] = None,
                hydration: float = None, burned: bool = None):
        return CellObject(veg=veg if veg else self.veg,
                          fire=fire if fire else self.fire,
                          fire_intensity=fire_intensity if fire_intensity else self.fire_intensity,
                          wind=wind if wind else self.wind,
                          hydration=hydration if hydration else self.hydration,
                          burned=burned if burned else self.burned)


def cell_state_description() -> None:
    """
    Prints the Label and Value for each member in the Enum
    """
    for name, value in VegetationType.__members__.items():
        print(f"{name}: {value.value}", end='; ')
    print()


class CellularAutomaton(ABC):
    """
    Class representing a forest as a grid but stored in 1d array
    """

    def __init__(self, rows: int, columns: int, wind: tuple[int, int] = (0, 0), seed: int = 1):
        """

        """
        self.grid = []
        self.rows = rows
        self.cols = columns
        self._done = False
        self._changed = False
        self._step = 0
        self.wind = wind
        self.random = random.Random()
        self.random.seed(seed)

        self.generate_grid()

    def generate_grid(self):
        for x in range(self.rows * self.cols):
            self.grid.append(
                CellObject(veg=VegetationType(self.random.randrange(3, 7)),
                           fire=0,
                           fire_intensity=0,
                           wind=self.wind,
                           hydration=0,
                           burned=False))

    

    def ignite(self, x: int, y: int) -> None:
        """
        Changes a given cell state to burning
        """
        index = self.i(x, y)
        self.grid[index] = self.grid[index].factory(fire=1)

    def get(self, x: int, y: int) -> CellObject | None:
        """
        Get a given cell state.

        Compute the 1d array index from x and y
        """
        if x < 0 or x > self.cols - 1:
            return None
        if y < 0 or y > self.rows - 1:
            return None

        return self.grid[self.i(x, y)]

    def _get(self, i: int) -> CellObject | None:
        """
        Internal getter for 1d index
        """
        if i < 0 or i > ((self.cols * self.rows) - 1):
            return None
        return self.grid[i]

    def print(self):
        """
        Print function for debugging purposes
        """
        for row in range(0, self.rows):
            for cols in range(0, self.cols):
                print(f"{self.get(row, cols).value} ", end='')
            print()
        print()

    def data(self) -> List[List[int]]:
        """
        Return a 2d representation of the forest
        """
        data = []
        for y in range(0, self.rows):
            row_values = []
            for x in range(0, self.cols):
                cell = self.get(x, y)
                if cell.burned:
                    row_values.append(FrontEndValues.BURNED.value)
                elif cell.fire > 0:
                    row_values.append(FrontEndValues.BURNING.value)
                else:
                    row_values.append(cell.veg.value)
            data.append(row_values)
        return data

    def step(self) -> None:
        """
        Progress the fire with one step.
        This is done by applying the rule function for each cell.

        The rule function is what defines how the fire flows through the forrest
        """
        self._changed = False
        self._step = self._step + 1
        new_grid = [self.rule(self.xy(i)) for i, c in enumerate(self.grid)]
        self.grid = new_grid

        self._done = not self._changed
    
    def run(self, do_print: bool) -> None:
        """
        Print and Step until Done
        """
        while not self._done:
            if do_print:
                self.print()
            self.step()

        print(f"Finished in {self._step} steps")

    def xy(self, index: int) -> Tuple[int, int]:
        """
        Convert index to (x,y) coordinate
        """
        x = index % self.cols
        y = int(index / self.cols)
        return x, y

    def i(self, x: int, y: int) -> int:
        """Compute index from coordinates

        Args:
            x (int): x-coordinate
            y (int): y-coordinate

        Returns:
            int: index
        """
        return x + y * self.cols

    def done(self) -> bool:
        """
        Return True if there is no more burning cells
        """
        return self._done

    @classmethod
    @abstractmethod
    def rule(cls, xy: Tuple[int, int]):
        """
        Override
        """
        pass
