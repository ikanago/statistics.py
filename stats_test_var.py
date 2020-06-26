import math

import click
from scipy import stats

import stats_test


def test_variance(n: int, target_variance: float, sample_variance: float, significance: float) -> (bool, float):
    """
    分散に関するカイ2乗検定を行う．

    ## Parameters  
    `n`: 標本の大きさ  
    `target_variance`: 帰無仮説において等しいと仮定する分散  
    `sample_variance`: 標本分散  
    `significance`: 有意水準

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか  
    `x`: 実現値
    """
    x = n * sample_variance / target_variance
    df = n - 1
    bottom = stats.chi2.ppf(significance / 2, df)
    top = stats.chi2.ppf(1 - significance / 2, df)
    side = "double"
    is_reject = stats_test.is_reject(
        x, stats_test.side_from_str(side), bottom, top, None, None)
    return (is_reject, x)


@click.command()
@click.option("-n", type=int, default=0, help="標本の大きさ")
@click.option("-h", "--hypothesis", type=float, default=0, help="帰無仮説で等しいと仮定する分散")
@click.option("-vr", "--variance", type=float, default=0, help="標本分散")
@click.option("-sd", "--stdev", type=float, default=0, help="標本標準偏差")
@click.option("-l", "--level", type=float, default=0.05, help="有意水準(default: 0.05)")
def cmd(n: int, hypothesis: float, variance: float, stdev: float, level: float):
    if level <= 0 or level >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    if variance <= 0:
        variance = math.pow(stdev, 2)
    (is_reject, test_stat) = test_variance(n, hypothesis, variance, level)

    print(stats_test.show_result(
        is_reject, test_stat, "σ", "{}".format(hypothesis)))


def main():
    cmd()


if __name__ == "__main__":
    main()
