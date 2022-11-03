from ca.cellular_automaton import CellObject, CellularAutomaton, VegetationType
from bresenham import bresenham

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

    def fire_rule(self, new: CellObject, original: CellObject, x: int, y: int):
        # Let's make it burn for one round if N, S, E or W cell are burning
        if original.hydration > 1:
            new = new.factory(fire = 0) #hydration = original.hydration - 1
            print("cell", new.fire, new.hydration)
        
        elif original.burned:
            new = new.factory()
            
        
        elif original.fire:
            #print("original.fire hydro", original.hydration)
            new = new.factory(fire = original.fire + 1)
        else:
            #print("hydro homie", original.hydration)
            (x_wind, y_wind) = new.wind
            # gets the list of cells the vector goes through
            # https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
            cells = list(bresenham(x, y, x-x_wind, y-y_wind))
            # the hydration checks can be removed if i can set the property to 0.
            # check normal boundaries
            if len([True for (x, y) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if self.get(x, y) is not None and self.get(x, y).fire > 0 and self.get(x, y).hydration < 2]) > 0:
                new = new.factory(fire = 1)
                pass
            
            # check cells in the wind direction
            for cell in cells:
                (x_cell, y_cell) = cell
                if self.get(x_cell, y_cell) is not None and self.get(x_cell, y_cell).fire > 0 and self.get(x_cell, y_cell).hydration < 2:
                    new = new.factory(fire = 1)
                    break

        return new

    def wind_rule(self, new, original, x, y):
        # not implemented yet
        pass


