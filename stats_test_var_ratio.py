import math

import click
from scipy import stats

import stats_test


def test_var_ratio(n1: int, sample_variance1: float, n2: int, sample_variance2: float, significance: float) -> (bool, float):
    """
    分散比に関するF検定を行う．

    ## Parameters
    `n1`: 1つめの標本の大きさ
    `sample_variance1`: 1つめの標本の既知の母分散
    `n2`: 2つめの標本の大きさ
    `sample_variance2`: 2つめの標本の既知の母分散
    `significance`: 有意水準

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか
    `z`: 実現値
    """

    f = n1 * (n2 - 1) * sample_variance1 / (n2 * (n1 - 1) * sample_variance2)
    df1 = n1 - 1
    df2 = n2 - 1
    bottom = stats.f.ppf(significance / 2, df1, df2)
    top = stats.f.ppf(1 - significance / 2, df1, df2)
    side = "double"
    is_reject = stats_test.is_reject(
        f, stats_test.side_from_str(side), bottom, top, None, None)
    return (is_reject, f)


@click.command()
@click.option("-n1", type=int, default=0, help="1つめの標本のデータの大きさ")
@click.option("-vr1", "--variance1", type=float, default=0, help="1つめの標本の標本分散")
@click.option("-sd1", "--stdev1", type=float, default=0, help="1つめの標本の標本標準偏差")
@click.option("-n2", type=int, default=0, help="2つめの標本のデータの大きさ")
@click.option("-vr2", "--variance2", type=float, default=0, help="2つめの標本の標本分散")
@click.option("-sd2", "--stdev2", type=float, default=0, help="2つめの標本の標本標準偏差")
@click.option("-l", "--level", type=float, default=0.05, help="有意水準(default: 0.05)")
def cmd(n1: int, variance1: float, stdev1: float, n2: int, variance2: float, stdev2: float, level: float):
    if level <= 0 or level >= 1:
        import sys
        print("有意水準は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    if variance1 <= 0:
        variance1 = math.pow(stdev1, 2)
    if variance2 <= 0:
        variance2 = math.pow(stdev2, 2)
    (is_reject, test_stat) = test_var_ratio(n1, variance1, n2, variance2, level)

    print(stats_test.show_result(is_reject, test_stat, "σ1", "σ2"))


def main():
    cmd()


if __name__ == "__main__":
    main()
