from unittest import TestCase

import math
import stats_test
import stats_test_mean


class TestStatsTestMean(TestCase):
    def test_stats_test_mean_with_pop_var1(self):
        n = 30
        hypothesis = 60
        mean = 56.75
        pop_variance = math.pow(15, 2)
        level = 0.95
        side = "double"
        (is_reject, test_stat) = stats_test_mean.test_mean_with_pop_variance(
            n, hypothesis, mean, pop_variance, level, stats_test.side_from_str(side))

        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, -1.187, places=3)

    def test_stats_test_mean_with_pop_var2(self):
        n = 50
        hypothesis = 30
        mean = 28.1
        pop_variance = 60
        level = 0.95
        side = "left"
        (is_reject, test_stat) = stats_test_mean.test_mean_with_pop_variance(
            n, hypothesis, mean, pop_variance, level, stats_test.side_from_str(side))

        self.assertTrue(is_reject)
        self.assertAlmostEqual(test_stat, -1.734, places=3)
