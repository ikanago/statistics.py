import csv
import math
from decimal import ROUND_HALF_UP, Decimal

import click
import numpy as np
from scipy import stats

from describe import describe


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
    chi2_lower = stats.chi2.ppf((1 + confidence) / 2.0, df)
    chi2_higher = stats.chi2.ppf((1 - confidence) / 2.0, df)
    bottom = n * sample_variance / float(chi2_lower)
    top = n * sample_variance / float(chi2_higher)
    return (bottom, top)


def estimate_all(n: int, sample_mean: float, sample_variance: float, pop_variance: float, confidence: float):
    resutl_str = ""
    if pop_variance > 0:
        bottom, top = interval_estimate_mean_with_pop_variance(
            sample_mean, pop_variance, n, confidence)
        resutl_str += "母平均の{}%信頼区間(母分散既知): [ {}, {} ]\n".format(
            int(confidence * 100), bottom, top)

    bottom, top = interval_estimate_mean_without_pop_variance(
        sample_mean, sample_variance, n, confidence)
    resutl_str += "母平均の{}%信頼区間(母分散未知): [ {}, {} ]\n".format(
        int(confidence * 100), bottom, top)

    bottom, top = interval_estimate_variance(
        sample_variance, n, confidence)
    resutl_str += "母分散の{}%信頼区間            : [ {}, {} ]\n".format(
        int(confidence * 100), bottom, top)

    return resutl_str


@click.command()
@click.option("-f", "--file", type=click.Path(exists=True), default="data.csv")
@click.option("-p", "--pop_variance", type=float, default=0, help="既知の母分散")
@click.option("-c", "--confidence", type=float, default=0.95, help="信頼係数(default: 0.95)")
def cmd(file, pop_variance: float, confidence: float):
    with open(file) as f:
        reader = csv.reader(f)
        # 2-dimensional array, but each row can be different number of elements.
        contents = [[float(v) for v in row] for row in reader]
        for i, row in enumerate(contents):
            n, sample_mean, sample_var, _ = describe(row)
            result = estimate_all(n, sample_mean, sample_var, pop_variance, confidence)
            print("系列{}".format(i + 1))
            print(result)


def main():
    cmd()


if __name__ == "__main__":
    main()
