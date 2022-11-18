from typing import Callable, Tuple

from ca.cellular_automaton import CellObject, CellularAutomaton, VegetationType
from bresenham import bresenham


class ForestSettings(object):

    def __init__(self,
                 veg_low_burn_time: int,
                 veg_medium_burn_time: int,
                 veg_high_burn_time: int,
                 spread_after: int,
                 wind: Tuple[int, int],
                 seed: int,
                 determine_burn_factor: Callable[[CellObject, Tuple[int, int]], float] = None,
                 **kwargs) -> None:
        self.seed = seed
        self.wind = wind
        self.determine_burn_factor = determine_burn_factor
        self.spread_after = spread_after
        self.veg_high_burn_time = veg_high_burn_time
        self.veg_low_burn_time = veg_low_burn_time
        self.veg_medium_burn_time = veg_medium_burn_time


class SimpleCa(CellularAutomaton):

    def __init__(self, rows: int, columns: int, settings: ForestSettings):
        super().__init__(rows, columns, settings.wind, settings.seed)
        self.settings = settings

    def rule(self, xy):
        """
        The `rule` function determines what the next state of a cell should be.

        The decision can be based on:
        * Neighbouring states
        * Wind
        * Dryness/wetness
        * And many more
        """
        (x, y) = xy
        original = self.get(x, y)
        new = original.factory()

        new = self.fire_rule(new, original, x, y)

        self._changed |= new != original
        return new

    def fire_rule(self, new: CellObject, original: CellObject, x: int, y: int) -> CellObject:
        """Determines how the fire should spread 

        Args:
            new (CellObject): New version of the cell
            original (CellObject): Original version of the cell for comparison
            x (int): row location
            y (int): column location

        Returns:
            CellObject: New version of the cell
        """
        # Fire does not spread before burning is 5
        if original.fire > 0:
            new = new.factory(fire=original.fire + 1)

        if original.burned or original.veg.value in [6, 7]:
            return new

        # Determine how long a single cell should burn depending on vegetation
        if VegetationType.LOW_VEG == original.veg and original.fire > self.settings.veg_low_burn_time:
            return new.factory(burned=True, fire_intensity=0)
        elif VegetationType.MED_VEG == original.veg and original.fire > self.settings.veg_medium_burn_time:
            return new.factory(burned=True, fire_intensity=0)
        elif VegetationType.HIGH_VEG == original.veg and original.fire > self.settings.veg_high_burn_time:
            return new.factory(burned=True, fire_intensity=0)
        else:
            pass

        # Should I burn?
        (x_wind, y_wind) = new.wind
        if original.fire > self.settings.spread_after:
            new = new.factory(fire_intensity=self.settings.determine_burn_factor(original, new.wind))
            return new

        summed_intensity = 0

        # gets the list of cells the vector goes through
        # https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
        cells = list(bresenham(x, y, x - x_wind, y - y_wind))

        # check normal boundaries
        for (x_cell, y_cell) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if self.get(x_cell, y_cell) is not None:
                if not self.get(x_cell, y_cell).burned:
                    summed_intensity = summed_intensity + \
                                       self.get(x_cell, y_cell).fire_intensity

        # check cells in the wind direction
        for cell in cells:
            (x_cell, y_cell) = cell
            if self.get(x_cell, y_cell) is not None:
                if not self.get(x_cell, y_cell).burned:
                    summed_intensity = summed_intensity + self.get(x_cell, y_cell).fire_intensity

        lucky_number = self.random.randrange(0, 100)
        if summed_intensity > lucky_number:
            new = new.factory(fire=1, hydration=0)

        return new

    def wind_rule(self, new, original, x, y):
        # not implemented yet
        pass
