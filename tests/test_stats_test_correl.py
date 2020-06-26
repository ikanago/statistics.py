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
