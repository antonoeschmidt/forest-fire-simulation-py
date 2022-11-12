from ca.cellular_automaton import CellObject, CellularAutomaton, VegetationType
from bresenham import bresenham
import math
import random


class SimpleCa(CellularAutomaton):
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
            CellObject: New verison of the cell
        """
        # Fire does not spread before burning is 5
        if original.fire > 0:
            new = new.factory(fire=original.fire + 1)

        if original.burned:
            return new

        # Determine how long a single cell should burned depending on vegation
        if VegetationType.LOW_VEG.value == original.veg and original.fire > 10:
            return new.factory(burned=True, fire_intensity=0)
        elif VegetationType.MED_VEG.value == original.veg and original.fire > 15:
            return new.factory(burned=True, fire_intensity=0)
        elif VegetationType.HIGH_VEG.value == original.veg and original.fire > 20:
            return new.factory(burned=True, fire_intensity=0)
        else:
            pass

        # Should I burn?
        (x_wind, y_wind) = new.wind

        wind_strength = math.sqrt(x_wind ** 2 + y_wind ** 2)
        wind_strength = wind_strength * 3
        if original.fire > 0:
            # Fire Intensity ===========================================================================================
            # 🪵 More wood == more fire 🔥
            burn_factor = 0
            if VegetationType.LOW_VEG.value == original.veg:
                burn_factor = 10
            elif VegetationType.MED_VEG.value == original.veg:
                burn_factor = 20
            elif VegetationType.HIGH_VEG.value == original.veg:
                burn_factor = 30
            else:
                pass

            new = new.factory(fire_intensity=wind_strength + burn_factor)
            return new  # I'm already burning

        summed_intensity = 0

        # gets the list of cells the vector goes through
        # https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
        cells = list(bresenham(x, y, x - x_wind, y - y_wind))

        # check normal boundaries
        for (x_cell, y_cell) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if self.get(x_cell, y_cell) is not None:
                summed_intensity = summed_intensity + \
                                   self.get(x_cell, y_cell).fire_intensity

        # check cells in the wind direction
        for cell in cells:
            (x_cell, y_cell) = cell
            if self.get(x_cell, y_cell) is not None:
                summed_intensity = summed_intensity + self.get(x_cell, y_cell).fire_intensity

        lucky_number = random.randrange(0, 100)
        if summed_intensity > lucky_number:
            new = new.factory(fire=1)

        return new

    def wind_rule(self, new, original, x, y):
        # not implemented yet
        pass
