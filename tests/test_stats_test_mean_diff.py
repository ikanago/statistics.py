from unittest import TestCase

import math
import stats_test
import stats_test_mean_diff


class TestStatsTestMeanDiff(TestCase):
    def test_stats_test_mean_diff_with_pop_var1(self):
        n1 = 40
        mean1 = 103
        variance1 = math.pow(15, 2)
        n2 = 35
        mean2 = 101
        variance2 = math.pow(15, 2)
        significance = 0.05
        (is_reject, test_stat) = stats_test_mean_diff.test_mean_diff_with_pop_variance(
            n1, mean1, variance1, n2, mean2, variance2, significance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, 0.576, places=3)

    def test_stats_test_mean_diff_with_pop_var2(self):
        n1 = 12
        mean1 = 420.6
        variance1 = math.pow(85, 2)
        n2 = 16
        mean2 = 450.4
        variance2 = math.pow(85, 2)
        significance = 0.05
        (is_reject, test_stat) = stats_test_mean_diff.test_mean_diff_with_pop_variance(
            n1, mean1, variance1, n2, mean2, variance2, significance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, -0.918, places=3)

    def test_stats_test_mean_diff_without_pop_var1(self):
        n1 = 15
        mean1 = 68.4
        variance1 = math.pow(10.2, 2)
        n2 = 21
        mean2 = 64.3
        variance2 = math.pow(9.3, 2)
        significance = 0.05
        (is_reject, test_stat) = stats_test_mean_diff.test_mean_diff_without_pop_variance(
            n1, mean1, variance1, n2, mean2, variance2, significance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, 1.217, places=3)

    def test_stats_test_mean_diff_without_pop_var2(self):
        n1 = 30
        mean1 = 5.2
        variance1 = math.pow(2.4, 2)
        n2 = 30
        mean2 = 7.5
        variance2 = math.pow(1.7, 2)
        significance = 0.05
        (is_reject, test_stat) = stats_test_mean_diff.test_mean_diff_without_pop_variance(
            n1, mean1, variance1, n2, mean2, variance2, significance)
        self.assertTrue(is_reject)
        self.assertAlmostEqual(test_stat, -4.211, places=3)

    def test_stats_test_mean_diff_with_big_sample1(self):
        n1 = 50
        mean1 = 60.5
        variance1 = math.pow(8.2, 2)
        n2 = 70
        mean2 = 55.2
        variance2 = math.pow(7.7, 2)
        significance = 0.05
        (is_reject, test_stat) = stats_test_mean_diff.test_mean_diff_with_big_sample(
            n1, mean1, variance1, n2, mean2, variance2, significance)
        self.assertTrue(is_reject)
        self.assertAlmostEqual(test_stat, 3.548, places=3)

    def test_stats_test_mean_diff_with_big_sample2(self):
        n1 = 120
        mean1 = 83.2
        variance1 = math.pow(16.8, 2)
        n2 = 90
        mean2 = 74.5
        variance2 = math.pow(12.5, 2)
        significance = 0.05
        (is_reject, test_stat) = stats_test_mean_diff.test_mean_diff_with_big_sample(
            n1, mean1, variance1, n2, mean2, variance2, significance)
        self.assertTrue(is_reject)
        self.assertAlmostEqual(test_stat, 4.282, places=3)
