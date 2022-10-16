import unittest

from ca.cellular_automaton import CellState
from ca.simple_fire import SimpleCa


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.rows = 10
        self.cols = 15
        self.ca = SimpleCa(self.rows, self.cols)

    def test_is_burning(self):
        self.ca.ignite(2, 2)
        self.assertEqual(self.ca.get(2, 2), CellState.BURNING)

    def test_is_not_burning(self):
        for r in range(0, 10):
            for c in range(0, 10):
                self.assertNotEqual(self.ca.get(r, c), CellState.BURNING)

    def test_xy(self):
        self.assertEqual(self.ca.xy(0), (0, 0))
        self.assertEqual(self.ca.xy(10), (10, 0))
        self.assertEqual(self.ca.xy(self.rows * self.cols - 1), (self.cols - 1, self.rows - 1))
