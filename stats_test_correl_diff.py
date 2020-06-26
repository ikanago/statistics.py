import math

import click
from scipy import stats

import stats_test


def test_correl_diff(n1: int, n2: int, r1: float, r2: float, significance: float) -> (bool, float):
    """
    相関係数に関するz検定を行う．

    ## Parameters  
    `n`: 標本の大きさ  
    `target_r`: 帰無仮説で等しいと仮定する相関係数  
    `r`: 標本相関係数  
    `significance`: 有意水準  

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか  
    `z`: 実現値
    """

    x1 = math.log((1 + r1) / (1 - r1)) / 2.0
    x2 = math.log((1 + r2) / (1 - r2)) / 2.0
    z = (x1 - x2) / math.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    bottom = stats.norm.ppf(significance / 2)
    top = stats.norm.ppf(1 - significance / 2)
    side = stats_test.side_from_str("double")
    is_reject = stats_test.is_reject(
        z, side, bottom, top, None, None)
    return (is_reject, z)


@click.command()
@click.option("-n1", type=int, default=0, help="1つめの標本の大きさ")
@click.option("-n2", type=int, default=0, help="2つめの標本の大きさ")
@click.option("-r1", type=float, default=0, help="1つめの標本の標本相関係数")
@click.option("-r2", type=float, default=0, help="2つめの標本の標本相関係数")
@click.option("-l", "--level", type=float, default=0.05, help="有意水準(default: 0.05)")
def cmd(n1: int, n2: int, r1: float, r2: float, level: float):
    if level <= 0 or level >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    (is_reject, test_stat) = test_correl_diff(n1, n2, r1, r2, level)

    print(stats_test.show_result(is_reject, test_stat, "r1", "r2"))


def main():
    cmd()


if __name__ == "__main__":
    main()
