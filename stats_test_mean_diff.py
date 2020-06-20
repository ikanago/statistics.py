import math

import click
from scipy import stats

import stats_test


def test_mean_diff_with_pop_variance(n1: int, mean1: float, pop_variance1: float, n2: int, mean2: float, pop_variance2: float, significance: float) -> (bool, float):
    """
    母分散既知において平均値の差に関するz検定を行う．

    ## Parameters
    `n1`: 1つめの標本の大きさ
    `mean1`: 1つめの標本の標本平均
    `pop_variance1`: 1つめの標本の既知の母分散
    `n2`: 2つめの標本の大きさ
    `mean2`: 2つめの標本の標本平均
    `pop_variance2`: 2つめの標本の既知の母分散
    `significance`: 有意水準

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか
    `z`: 実現値
    """

    z = (mean1 - mean2) / math.sqrt(pop_variance1 / n1 + pop_variance2 / n2)
    bottom = stats.norm.ppf((1 - significance) / 2)
    top = stats.norm.ppf((1 + significance) / 2)
    side = "double"
    is_reject = stats_test.is_reject(
        z, stats_test.side_from_str(side), bottom, top, None, None)
    return (is_reject, z)


@click.command()
@click.option("-z", "--z_test", is_flag=True, help="既知の母分散を使うかどうか")
@click.option("-n1", type=int, default=0, help="1つめの標本のデータの大きさ")
@click.option("-m1", "--mean1", type=float, default=0, help="1つめの標本の標本平均")
@click.option("-vr1", "--variance1", type=float, default=0, help="1つめの標本の既知の母分散")
@click.option("-sd1", "--stdev1", type=float, default=0, help="1つめの標本の既知の母標準偏差")
@click.option("-n2", type=int, default=0, help="2つめの標本のデータの大きさ")
@click.option("-m2", "--mean2", type=float, default=0, help="2つめの標本の標本平均")
@click.option("-vr2", "--variance2", type=float, default=0, help="2つめの標本の既知の母分散")
@click.option("-sd2", "--stdev2", type=float, default=0, help="2つめの標本の既知の母標準偏差")
@click.option("-l", "--level", type=float, default=0.95, help="有意水準(default: 0.95)")
def cmd(z_test: bool, n1: int, mean1: float, variance1: float, stdev1: float, n2: int, mean2: float, variance2: float, stdev2: float, level: float):
    if level <= 0 or level >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    if variance1 <= 0:
        variance1 = math.pow(stdev1, 2)
    if variance2 <= 0:
        variance2 = math.pow(stdev2, 2)

    if z_test:
        (is_reject, test_stat) = test_mean_diff_with_pop_variance(
            n1, mean1, variance1, n2, mean2, variance2, level)

    print(stats_test.show_result(is_reject, test_stat, "μ1", "μ2"))


def main():
    cmd()


if __name__ == "__main__":
    main()
