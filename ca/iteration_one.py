from ca.cellular_automaton import CellObject, CellularAutomaton
from ca.simple_cell import ForestSettings


class IterationOne(CellularAutomaton):

    def __init__(self, rows: int, columns: int, settings: ForestSettings, stat_file: str):
        super().__init__(rows, columns, settings.wind, settings.seed, stat_file=stat_file)
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

        changed = (new.fire > original.fire or new.burned != original.burned)
        self._changed |= changed
        return new

    def fire_rule(self, new: CellObject, original: CellObject, x: int, y: int):
        # Let's make it burn for one round if N, S, E or W cell are burning
        if original.burned:
            new = new.factory()
        if original.fire:
            new = new.factory(fire=original.fire + 1)
        else:
            # check normal boundaries
            if len([True for (x, y) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
                    self.get(x, y) is not None and self.get(x, y).fire > 0]) > 0:
                new = new.factory(fire=1)

        return new
