import argparse
import csv

import click
import numpy as np

import interval_estimation
import stats_test
from describe import describe


@click.group()
@click.option("-f", "--file", type=click.Path(exists=True), default="data.csv")
@click.pass_context
def cmd(ctx, file):
    with open(file) as f:
        reader = csv.reader(f)
        # 2-dimensional array, but each row can be different number of elements.
        contents = [[float(v) for v in row] for row in reader]
        data = contents
        ctx.obj["data"] = data


@cmd.command()
@click.option("-n", type=int, default=0, help="データの大きさ")
@click.option("-h", "--hypothesis", type=float, default=0, help="帰無仮説で等しいと仮定する平均")
@click.option("-m", "--mean", type=float, default=0, help="標本平均")
@click.option("-p", "--pop_variance", type=float, default=0, help="既知の母分散")
@click.option("-l", "--level", type=float, default=0.95, help="有意水準(default: 0.95)")
@click.option("-s", "--side", type=click.Choice(["double", "left", "right"]), default="double", help="検定方法(両側，左片側，右片側)")
def test_mean(n: int, hypothesis: float, mean: float, pop_variance: float, level: float, side: str):
    if level <= 0 or level >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    (is_reject, test_stat) = stats_test.test_mean_with_pop_variance(
        n, hypothesis, mean, pop_variance, level, side_from_str(side))
    if is_reject:
        print("帰無仮説 'μ = {}' は棄却されました{}".format(hypothesis, test_stat))
    else:
        print("帰無仮説 'μ = {}' は採択されました{}".format(hypothesis, test_stat))


def main():
    cmd(obj={})


if __name__ == "__main__":
    main()
