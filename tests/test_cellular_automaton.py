import unittest

from ca.ca import CellularAutomaton, CellState


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.rows = 10
        self.cols = 15
        self.ca = CellularAutomaton(self.rows, self.cols)

    def test_is_burning(self):
        self.ca.ignite(2, 2)
        self.assertEqual(self.ca.get(2, 2), CellState.BURNING)

    def test_is_not_burning(self):
        for r in range(0, 10):
            for c in range(0, 10):
                self.assertNotEqual(self.ca.get(r, c), CellState.BURNING)
