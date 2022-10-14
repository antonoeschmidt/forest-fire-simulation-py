from enum import Enum
from traceback import print_tb
import asyncio
import time
import websockets
import json

from ca.ca import CellState, CellularAutomaton


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
        # Let's make it burn for one round if N, S, E or W cell are burning
        (x, y) = xy
        original = self.get(x, y)
        new = original

        if original == CellState.BURNING or original == CellState.EMPTY:
            new = CellState.EMPTY

        elif CellState.BURNING in [self.get(x, y) for (x, y) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]]:
            new = CellState.BURNING

        self._changed |= new != original
        return new
