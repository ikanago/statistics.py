import numpy as np

from describe import describe
from interval_estimation import (interval_estimate_mean_with_pop_variance,
                                 interval_estimate_mean_without_pop_variance,
                                 interval_estimate_variance)


def prompt_describe(data: list):
    length, sample_mean, sample_variance, unbiased_variance = describe(data)
    print("データ数: {}".format(length))
    print("標本平均: {}".format(sample_mean))
    print("標本分散: {}".format(sample_variance))
    print("不偏分散: {}".format(unbiased_variance))


def prompt_interval_estimate(n: int, sample_mean: float, sample_variance: float, pop_variance: float, confidence: float):
    if pop_variance > 0:
        bottom, top = interval_estimate_mean_with_pop_variance(
            sample_mean, pop_variance, n, confidence)
        print("母平均の{}%信頼区間(母分散既知): [ {}, {} ]".format(
            int(confidence * 100), bottom, top))

    bottom, top = interval_estimate_mean_without_pop_variance(
        sample_mean, sample_variance, n, confidence)
    print("母平均の{}%信頼区間(母分散未知): [ {}, {} ]".format(
        int(confidence * 100), bottom, top))

    bottom, top = interval_estimate_variance(
        sample_variance, n, confidence)
    print("母分散の{}%信頼区間            : [ {}, {} ]".format(
        int(confidence * 100), bottom, top))
