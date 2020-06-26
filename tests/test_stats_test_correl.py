from unittest import TestCase

import math
import stats_test
import stats_test_correl


class TestStatsTestCorrel(TestCase):
    def test_stats_test_no_correl(self):
        n = 25
        r = 0.352
        sigificance = 0.05
        (is_reject, test_stat) = stats_test_correl.test_no_correl(n, r, sigificance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, 1.804, places=3)

    def test_stats_test_correl(self):
        n = 48
        target_r = 0.7
        r = 0.648
        sigificance = 0.05
        (is_reject, test_stat) = stats_test_correl.test_correl(n, target_r, r, sigificance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, -0.640, places=3)
