from scipy import stats
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import math
import argparse

def normarize_variance(variance: float, n: int):
    return math.sqrt(variance / n)

def interval_estimate_mean_with_pop_variance(sample_mean: float, pop_variance: float, n: int, confidence: float):
    """
    母平均の95%信頼区間を求める．母分散は既知とする．

    ## Parameters
    sample_mean: 標本平均

    pop_variance: 母分散

    n: データ数

    confidence: 信頼係数

    ## Returns
    (bottom, top): 推定した信頼区間の下限と上限
    """
    normarized_varianse = normarize_variance(pop_variance, n)
    bottom, top = stats.norm.interval(confidence, loc=sample_mean, scale=normarized_varianse)
    return (bottom, top)

def interval_estimate_mean_without_pop_variance(sample_mean: float, sample_variance: float, n: int, confidence: float):
    """
    母平均の95%信頼区間を求める．母分散は未知とする．

    ## Parameters
    sample_mean: 標本平均

    sample_variance: 標本分散

    n: データ数

    confidence: 信頼係数

    ## Returns
    (bottom, top): 推定した信頼区間の下限と上限
    """
    df = n - 1
    normarized_variance = normarize_variance(sample_variance, df)
    bottom, top = stats.t.interval(confidence, loc=sample_mean, scale=normarized_variance, df=df)
    return (bottom, top)

def interval_estimate_variance(sample_variance: float, n: int, confidence: float):
    """
    母平均の95%信頼区間を求める．母分散は未知とする．

    ## Parameters
    sample_variance: 標本分散

    n: データ数

    confidence: 信頼係数

    ## Returns
    (bottom, top): 推定した信頼区間の下限と上限
    """
    df = n - 1
    chi2_lower = Decimal(stats.chi2.ppf((1 + confidence) / 2.0, df)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    chi2_higher = Decimal(stats.chi2.ppf((1 - confidence) / 2.0, df)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    bottom = n * sample_variance / float(chi2_lower)
    top = n * sample_variance / float(chi2_higher)
    return (bottom, top)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="data.csv", help="入力データの記録されたCSVファイルへのパス(default: data.csv).")
    parser.add_argument("-c", "--confidence", type=float, default=0.95, help="信頼係数(default: 0.95)")
    args = parser.parse_args()
    confidence = args.confidence
    if confidence <= 0 or confidence >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()
    
    data = np.array([12.4, 13.5, 12.7, 14.1, 13.8, 14.1, 12.0, 12.8, 13.1, 15.4])
    data_size = len(data)
    sample_mean = data.mean()
    sample_variance = data.var()
    unbiased_variance = data.var(ddof=1)
    print("標本平均: {}".format(sample_mean))
    print("標本分散: {}".format(sample_variance))
    print("不偏分散: {}".format(unbiased_variance))

    pop_variance = 625
    bottom, top = interval_estimate_mean_with_pop_variance(sample_mean, pop_variance, data_size, confidence)
    print("母平均の95%信頼区間(母分散既知): [ {}, {} ]".format(bottom, top))

    bottom, top = interval_estimate_mean_without_pop_variance(sample_mean, sample_variance, data_size, confidence)
    print("母平均の95%信頼区間(母分散未知): [ {}, {} ]".format(bottom, top))

    bottom, top = interval_estimate_variance(sample_variance, data_size, confidence)
    print("母分散の95%信頼区間            : [ {}, {} ]".format(bottom, top))


if __name__ == "__main__":
    main()
