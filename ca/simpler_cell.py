from ca.cellular_automaton import CellularAutomaton


class SimplerCa(CellularAutomaton):
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

        self._changed |= new != original
        return new
