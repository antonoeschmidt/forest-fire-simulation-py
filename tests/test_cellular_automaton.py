import unittest

from ca.simple_cell import SimpleCa


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.rows = 4
        self.cols = 8
        self.ca = SimpleCa(self.rows, self.cols)

    def test_is_burning_sym(self):
        self.ca.ignite(2, 2)
        self.assertTrue(self.ca.get(2, 2).fire > 0)

    def test_is_burning_asym(self):
        self.ca.ignite(5, 2)
        self.assertTrue(self.ca.get(5, 2).fire > 0)

    def test_is_burning_four_times(self):
        self.ca.ignite(1, 1)
        self.ca.ignite(2, 2)
        self.ca.ignite(3, 3)
        expected_burn_count = 3

        burn_count = 0
        for r in range(0, self.cols):
            for c in range(0, self.rows):
                if self.ca.get(r, c).fire > 0:
                    burn_count = burn_count + 1

        self.assertEqual(expected_burn_count, burn_count)
        self.assertTrue(self.ca.get(1, 1).fire > 0)
        self.assertTrue(self.ca.get(2, 2).fire > 0)
        self.assertTrue(self.ca.get(3, 3).fire > 0)

    def test_is_not_burning(self):
        for r in range(0, self.cols):
            for c in range(0, self.rows):
                # print(self.ca.get(r,c))
                print(f'{self.ca.i(r, c)} : {r}, {c}')
                self.assertFalse(self.ca.get(r, c).fire > 0)

    def test_xy(self):
        self.assertEqual(self.ca.xy(0), (0, 0))
        self.assertEqual(self.ca.xy(10), (2, 1))
        self.assertEqual(self.ca.xy(30), (6, 3))
        self.assertEqual(
            self.ca.xy(self.rows * self.cols - 1),
            (self.cols - 1, self.rows - 1))
