import math

import click
from scipy import stats

import stats_test


def test_mean_with_pop_variance(n: int, target_mean: float, sample_mean: float, pop_variance: float, significance: float, side: stats_test.Side) -> (bool, float):
    """
    平均値に関するz検定を行う．

    ## Parameters  
    `n`: 標本の大きさ  
    `target_mean`: 帰無仮説において等しいと仮定する平均値  
    `sample_mean`: 標本平均  
    `pop_variance`: 既知の母分散  
    `significance`: 有意水準  
    `side`: 棄却域の取り方

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか
    """

    z = (sample_mean - target_mean) / math.sqrt(pop_variance / n)
    bottom = stats.norm.ppf((1 - significance) / 2)
    top = stats.norm.ppf((1 + significance) / 2)
    bottom_left = stats.norm.ppf(1 - significance)
    top_right = stats.norm.ppf(significance)
    is_reject = stats_test.is_reject(z, side, bottom, top, bottom_left, top_right)
    return (is_reject, z)


@click.command()
@click.option("-n", type=int, default=0, help="データの大きさ")
@click.option("-h", "--hypothesis", type=float, default=0, help="帰無仮説で等しいと仮定する平均")
@click.option("-m", "--mean", type=float, default=0, help="標本平均")
@click.option("-p", "--pop_variance", type=float, default=0, help="既知の母分散")
@click.option("-l", "--level", type=float, default=0.95, help="有意水準(default: 0.95)")
@click.option("-s", "--side", type=click.Choice(["double", "left", "right"]), default="double", help="検定方法(両側，左片側，右片側)")
def cmd(n: int, hypothesis: float, mean: float, pop_variance: float, level: float, side: str):
    if level <= 0 or level >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    if pop_variance > 0:
        (is_reject, test_stat) = test_mean_with_pop_variance(
            n, hypothesis, mean, pop_variance, level, stats_test.side_from_str(side))

    (is_reject, test_stat) = test_mean_with_pop_variance(
        n, hypothesis, mean, pop_variance, level, stats_test.side_from_str(side))
    print(stats_test.show_result(is_reject, test_stat, hypothesis))


def main():
    cmd()


if __name__ == "__main__":
    main()
