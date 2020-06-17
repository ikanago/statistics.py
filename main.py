from scipy import stats
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import math

def normarize_variance(variance: float, n: int):
    return math.sqrt(variance / n)

def interval_estimate_mean_with_pop_variance(sample_mean: float, pop_variance: float, n: int):
    """
    母平均の95%信頼区間を求める．母分散は既知とする．

    ## Parameters
    sample_mean: 標本平均

    pop_variance: 母分散

    n: データ数
    ## Returns
    (bottom, top): 推定した95%信頼区間
    """
    normarized_varianse = normarize_variance(pop_variance, n)
    bottom, top = stats.norm.interval(0.95, loc=sample_mean, scale=normarized_varianse)
    return (bottom, top)

def interval_estimate_mean_without_pop_variance(sample_mean: float, sample_varianse: float, n: int):
    """
    母平均の95%信頼区間を求める．母分散は未知とする．

    ## Parameters
    sample_mean: 標本平均

    sample_variance: 標本分散

    n: データ数
    ## Returns
    (bottom, top): 推定した95%信頼区間
    """
    df = n - 1
    normarized_variance = normarize_variance(sample_varianse, df)
    bottom, top = stats.t.interval(0.95, loc=sample_mean, scale=normarized_variance, df=df)
    return (bottom, top)

def interval_estimate_variance(sample_variance: float, n: int):
    """
    母平均の95%信頼区間を求める．母分散は未知とする．

    ## Parameters
    sample_variance: 標本分散

    n: データ数
    ## Returns
    (bottom, top): 推定した95%信頼区間
    """
    df = n - 1
    chi2_lower = Decimal(stats.chi2.ppf(0.975, df)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    chi2_higher = Decimal(stats.chi2.ppf(0.025, df)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    bottom = n * sample_variance / float(chi2_lower)
    top = n * sample_variance / float(chi2_higher)
    return (bottom, top)

def main():
    data = np.array([100, 70, 30, 60, 50])
    data_size = len(data)
    sample_mean = data.mean()
    sample_variance = data.var()
    unbiased_variance = data.var(ddof=1)
    print("標本平均: {}".format(sample_mean))
    print("標本分散: {}".format(sample_variance))
    print("不偏分散: {}".format(unbiased_variance))

    pop_variance = 625
    bottom, top = interval_estimate_mean_with_pop_variance(sample_mean, pop_variance, data_size)
    print("母平均の95%信頼区間(母分散既知): [ {}, {} ]".format(bottom, top))

    bottom, top = interval_estimate_mean_without_pop_variance(sample_mean, sample_variance, data_size)
    print("母平均の95%信頼区間(母分散未知): [ {}, {} ]".format(bottom, top))

    bottom, top = interval_estimate_variance(sample_variance, data_size)
    print("母分散の95%信頼区間            : [ {}, {} ]".format(bottom, top))


if __name__ == "__main__":
    main()
