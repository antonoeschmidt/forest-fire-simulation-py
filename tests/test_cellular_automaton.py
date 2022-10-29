import unittest

from ca.cellular_automaton import CellState
from ca.simple_cell import SimpleCa


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.rows = 10
        self.cols = 15
        self.ca = SimpleCa(self.rows, self.cols)

    def test_is_burning_four_times(self):
        self.ca.ignite(2, 2)
        self.assertEqual(self.ca.get(2, 2), CellState.BURNING)

    def test_is_burning(self):
        self.ca.ignite(1, 1)
        self.ca.ignite(2, 2)
        self.ca.ignite(3, 3)
        self.ca.ignite(4, 4)
        expected_burn_count = 4

        burn_count = 0
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                if self.ca.get(r, c) == CellState.BURNING:
                    burn_count = burn_count + 1

        self.assertEqual(expected_burn_count, burn_count)
        self.assertEqual(self.ca.get(1, 1), CellState.BURNING)
        self.assertEqual(self.ca.get(2, 2), CellState.BURNING)
        self.assertEqual(self.ca.get(3, 3), CellState.BURNING)
        self.assertEqual(self.ca.get(4, 4), CellState.BURNING)

    def test_is_not_burning(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                self.assertNotEqual(self.ca.get(r, c), CellState.BURNING)

    def test_xy(self):
        self.assertEqual(self.ca.xy(0), (0, 0))
        self.assertEqual(self.ca.xy(10), (10, 0))
        self.assertEqual(self.ca.xy(self.rows * self.cols - 1), (self.cols - 1, self.rows - 1))
