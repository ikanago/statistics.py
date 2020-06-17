import numpy as np
from scipy import stats
from decimal import Decimal, ROUND_HALF_UP
import math


def normarize_variance(variance: float, n: int):
    return math.sqrt(variance / n)


def interval_estimate_mean_with_pop_variance(sample_mean: float, pop_variance: float, n: int, confidence: float) -> (float, float):
    """
    母平均の95%信頼区間を求める．母分散は既知とする．

    ## Parameters
    `sample_mean`: 標本平均

    `pop_variance`: 母分散

    `n`: データ数

    `confidence`: 信頼係数

    ## Returns
    (`bottom`, `top`): 推定した信頼区間の下限と上限
    """
    normarized_varianse = normarize_variance(pop_variance, n)
    bottom, top = stats.norm.interval(
        confidence, loc=sample_mean, scale=normarized_varianse)
    return (bottom, top)


def interval_estimate_mean_without_pop_variance(sample_mean: float, sample_variance: float, n: int, confidence: float) -> (float, float):
    """
    母平均の95%信頼区間を求める．母分散は未知とする．

    ## Parameters
    `sample_mean`: 標本平均

    `sample_variance`: 標本分散

    n: データ数

    `confidence`: 信頼係数

    ## Returns
    (`bottom`, `top`): 推定した信頼区間の下限と上限
    """
    df = n - 1
    normarized_variance = normarize_variance(sample_variance, df)
    bottom, top = stats.t.interval(
        confidence, loc=sample_mean, scale=normarized_variance, df=df)
    return (bottom, top)


def interval_estimate_variance(sample_variance: float, n: int, confidence: float) -> (float, float):
    """
    母平均の95%信頼区間を求める．母分散は未知とする．

    ## Parameters
    `sample_variance`: 標本分散

    `n`: データ数

    `confidence`: 信頼係数

    ## Returns
    (`bottom`, `top`): 推定した信頼区間の下限と上限
    """
    df = n - 1
    chi2_lower = Decimal(stats.chi2.ppf((1 + confidence) / 2.0, df)
                         ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    chi2_higher = Decimal(stats.chi2.ppf(
        (1 - confidence) / 2.0, df)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    bottom = n * sample_variance / float(chi2_lower)
    top = n * sample_variance / float(chi2_higher)
    return (bottom, top)
