from unittest import TestCase

import math
import stats_test
import stats_test_correl_diff


class TestStatsTestCorrelDiff(TestCase):
    def test_stats_test_correl_diff(self):
        n1 = 80
        n2 = 65
        r1 = 0.538
        r2 = 0.743
        sigificance = 0.05
        (is_reject, test_stat) = stats_test_correl_diff.test_correl_diff(
            n1, n2, r1, r2, sigificance)
        self.assertTrue(is_reject)
        self.assertAlmostEqual(test_stat, -2.085, places=3)
