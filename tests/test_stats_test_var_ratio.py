from unittest import TestCase

import math
import stats_test
import stats_test_var_ratio


class TestStatsTestVarRatio(TestCase):
    def test_stats_test_var_ratio1(self):
        n1 = 10
        sample_variance1 = 8.8
        n2 = 8
        sample_variance2 = 10.1
        significance = 0.10
        (is_reject, test_stat) = stats_test_var_ratio.test_var_ratio(n1, sample_variance1, n2, sample_variance2, significance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, 0.847, places=3)

    def test_stats_test_var_ratio2(self):
        n1 = 16
        sample_variance1 = 12.5
        n2 = 21
        sample_variance2 = 13.8
        significance = 0.05
        (is_reject, test_stat) = stats_test_var_ratio.test_var_ratio(n1, sample_variance1, n2, sample_variance2, significance)
        self.assertFalse(is_reject)
        self.assertAlmostEqual(test_stat, 0.92, places=3)
