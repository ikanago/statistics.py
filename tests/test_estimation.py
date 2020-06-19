from unittest import TestCase

import describe
import estimation


class TestEstimation(TestCase):
    def test_estimation(self):
        data = [100, 70, 30, 60, 50]
        length, mean, variance, _ = describe.describe(data)
        pop_variance = 625
        confidence = 0.95

        bottom, top = estimation.interval_estimate_mean_with_pop_variance(
            mean, pop_variance, length, confidence)
        self.assertAlmostEqual(bottom, 40.1, places=1)
        self.assertAlmostEqual(top, 83.9, places=1)

        bottom, top = estimation.interval_estimate_mean_without_pop_variance(
            mean, variance, length, confidence)
        self.assertAlmostEqual(bottom, 29.9, places=1)
        self.assertAlmostEqual(top, 94.1, places=1)

        bottom, top = estimation.interval_estimate_variance(
            variance, length, confidence)
        self.assertAlmostEqual(bottom, 241, places=0)
        self.assertAlmostEqual(top, 5532, places=0)
