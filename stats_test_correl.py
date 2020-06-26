import math

import click
from scipy import stats

import stats_test


def test_no_correl(n: int, r: float, significance: float) -> (bool, float):
    """
    無相関かどうかのt検定を行う．

    ## Parameters  
    `n`: 標本の大きさ  
    `r`: 標本相関係数  
    `significance`: 有意水準  

    ## Returns  
    `is_reject`: 帰無仮説が棄却されるかどうか  
    `t`: 実現値
    """

    df = n - 2
    t = r * math.sqrt(df) / math.sqrt(1 - math.pow(r, 2))
    bottom = stats.t.ppf(significance / 2, df)
    top = stats.t.ppf(1 - significance / 2, df)
    side = stats_test.side_from_str("double")
    is_reject = stats_test.is_reject(
        t, side, bottom, top, None, None)
    return (is_reject, t)


def test_correl(n: int, target_r: float, r: float, significance: float) -> (bool, float):
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

    x = math.log((1 + r) / (1 - r)) / 2.0
    xi = math.log((1 + target_r) / (1 - target_r)) / 2.0
    z = (x - xi) * math.sqrt(n - 3)
    bottom = stats.norm.ppf(significance / 2)
    top = stats.norm.ppf(1 - significance / 2)
    side = stats_test.side_from_str("double")
    is_reject = stats_test.is_reject(
        z, side, bottom, top, None, None)
    return (is_reject, z)


@click.command()
@click.option("-n", type=int, default=0, help="標本の大きさ")
@click.option("-h", "--hypothesis", type=float, default=0, help="帰無仮説で等しいと仮定する相関係数")
@click.option("-r", type=float, default=0, help="標本相関係数")
@click.option("-l", "--level", type=float, default=0.05, help="有意水準(default: 0.05)")
def cmd(n: int, hypothesis: float, r: float, level: float):
    if level <= 0 or level >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    if hypothesis == 0.0:
        (is_reject, test_stat) = test_no_correl(n, r, level)
    else:
        if hypothesis >= 1.0:
            import sys
            print("相関係数1の帰無仮説における検定はできません．", file=sys.stderr)
            exit()
        (is_reject, test_stat) = test_correl(n, hypothesis, r, level)

    print(stats_test.show_result(is_reject, test_stat, "r", hypothesis))


def main():
    cmd()


if __name__ == "__main__":
    main()
