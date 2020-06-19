from unittest import TestCase

import describe


class TestDescribe(TestCase):
    def test_describe(self):
        data = [60, 80, 80, 60, 60, 100, 50, 60, 70, 70]
        expected_length = 10
        expected_mean = 69
        expected_var = 189
        expected_unbiased_var = 210
        length, mean, var, unbiased_var = describe.describe(data)
        self.assertEqual(expected_length, length)
        self.assertAlmostEqual(expected_mean, mean)
        self.assertAlmostEqual(expected_var, var)
        self.assertAlmostEqual(expected_unbiased_var, unbiased_var)
