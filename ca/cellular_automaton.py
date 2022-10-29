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
    wind: Tuple[int, int]
    hydration: float
    burned: bool
    
    def factory(self, veg: int = None, fire: int = None, wind: Tuple[int, int] = None, 
                                        hydration: float = None, burned: bool = None):

        return CellObject(veg = veg if veg else self.veg,  
                        fire = fire if fire else self.fire,
                        wind = wind if wind else self.wind,
                        hydration = hydration if hydration else self.hydration,
                        burned = burned if burned else self.burned)

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

    def __init__(self, n: int, m: int, wind: tuple[int, int] = (0,0)):
        """

        """
        self.rows = n
        self.cols = m
        self._done = False
        self._changed = False
        self._step = 0
        self.wind = wind

        self.grid = [CellObject(veg = VegetationType.MED_VEG, fire = 0, wind = wind, hydration = 0, burned = False) 
                                                                        for x in range(0, self.rows * self.cols)]

    def ignite(self, x: int, y: int) -> None:
        """
        Changes a given cell state to burning
        """
        index = self.cols * x + y
        self.grid[index] = self.grid[index].factory(fire=1)

    def get(self, x: int, y: int) -> CellObject:
        """
        Get a given cell state.

        Compute the 1d array index from x and y
        """
        if x < 0 or x > self.rows - 1:
            return None
        if y < 0 or y > self.cols - 1:
            return None

        index = x * self.cols + y
        return self.grid[index]

    def _get(self, i: int) -> CellObject:
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
                print(f"{self._get(self.cols * row + cols).value} ", end='')
            print()
        print()

    def data(self) -> List[List[int]]:
        """
        Return a 2d representation of the forest
        """
        data = []
        for row in range(0, self.rows):
            row_values = []
            for cols in range(0, self.cols):
                cell = self._get(self.cols * row + cols)
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
        col = index % self.cols
        row = int(index / self.cols)
        return col, row

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
