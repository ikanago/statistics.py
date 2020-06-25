import math

import click
from scipy import stats

import stats_test


def test_mean_with_pop_variance(n: int, target_mean: float, sample_mean: float, pop_stdev: float, significance: float, side: stats_test.Side) -> (bool, float):
    """
    母分散既知において平均値に関するz検定を行う．

    ## Parameters  
    `n`: 標本の大きさ  
    `target_mean`: 帰無仮説において等しいと仮定する平均値  
    `sample_mean`: 標本平均  
    `sample_stdev`: 既知の標本標準偏差  
    `significance`: 有意水準  
    `side`: 棄却域の取り方

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか  
    `z`: 実現値
    """

    z = (sample_mean - target_mean) / (pop_stdev / math.sqrt(n))
    bottom = stats.norm.ppf(significance / 2)
    top = stats.norm.ppf(1 + significance / 2)
    bottom_left = stats.norm.ppf(1 - significance)
    top_right = stats.norm.ppf(significance)
    is_reject = stats_test.is_reject(
        z, side, bottom, top, bottom_left, top_right)
    return (is_reject, z)


def test_mean_without_pop_variance(n: int, target_mean: float, sample_mean: float, sample_stdev: float, significance: float, side: stats_test.Side) -> (bool, float):
    """
    平均値に関するt検定を行う．

    ## Parameters  
    `n`: 標本の大きさ  
    `target_mean`: 帰無仮説において等しいと仮定する平均値  
    `sample_mean`: 標本平均  
    `sample_stdev`: 標本標準偏差  
    `significance`: 有意水準  
    `side`: 棄却域の取り方

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか
    `t`: 実現値
    """

    t = (sample_mean - target_mean) / (sample_stdev / math.sqrt(n - 1))
    df = n - 1
    bottom = stats.t.ppf(significance / 2, df)
    top = stats.t.ppf(1 - significance / 2, df)
    bottom_left = stats.t.ppf(1 - significance, df)
    top_right = stats.t.ppf(significance, df)
    is_reject = stats_test.is_reject(
        t, side, bottom, top, bottom_left, top_right)
    return (is_reject, t)


@click.command()
@click.option("-z", "--z_test", is_flag=True, help="既知の母分散を使うかどうか")
@click.option("-n", type=int, default=0, help="データの大きさ")
@click.option("-h", "--hypothesis", type=float, default=0, help="帰無仮説で等しいと仮定する平均")
@click.option("-m", "--mean", type=float, default=0, help="標本平均")
@click.option("-vr", "--variance", type=float, default=0, help="既知の母分散/標本分散")
@click.option("-sd", "--stdev", type=float, default=0, help="既知の母標準偏差/標本標準偏差")
@click.option("-l", "--level", type=float, default=0.05, help="有意水準(default: 0.05)")
@click.option("-s", "--side", type=click.Choice(["double", "left", "right"]), default="double", help="検定方法(両側，左片側，右片側)")
def cmd(z_test: bool, n: int, hypothesis: float, mean: float, variance: float, stdev: float, level: float, side: str):
    if level <= 0 or level >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    if stdev <= 0:
        stdev = math.sqrt(variance)

    if z_test:
        (is_reject, test_stat) = test_mean_with_pop_variance(
            n, hypothesis, mean, stdev, level, stats_test.side_from_str(side))
    else:
        (is_reject, test_stat) = test_mean_without_pop_variance(
            n, hypothesis, mean, stdev, level, stats_test.side_from_str(side))

    print(stats_test.show_result(is_reject, test_stat, "μ", hypothesis))


def main():
    cmd()


if __name__ == "__main__":
    main()
