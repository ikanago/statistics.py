from unittest import TestCase

import math
import stats_test
import stats_test_var


class TestStatsTestVar(TestCase):
    def test_stats_test_var1(self):
        n = 10
        target_variance = 0.090
        sample_variance = 0.107949
        significance = 0.05
        (is_reject, test_stat) = stats_test_var.test_variance(
            n, target_variance, sample_variance, significance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, 11.992, places=2)

    def test_stats_test_var2(self):
        n = 50
        target_variance = math.pow(10, 2)
        sample_variance = math.pow(8.8, 2)
        significance = 0.05
        (is_reject, test_stat) = stats_test_var.test_variance(
            n, target_variance, sample_variance, significance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, 38.721, places=2)
