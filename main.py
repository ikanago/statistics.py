import argparse
import csv

import click
import numpy as np

import interval_estimation
import prompt
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
@click.pass_context
def desc(ctx):
    data = ctx.obj["data"]
    for i, array in enumerate(data):
        print("系列{}".format(i + 1))
        prompt.prompt_describe(array)
        print()


@cmd.command()
@click.pass_context
@click.option("-p", "--pop_variance", type=float, default=0, help="既知の母分散")
@click.option("-c", "--confidence", type=float, default=0.95, help="信頼係数(default: 0.95)")
def est(ctx, pop_variance: float, confidence: float):
    data = ctx.obj["data"]
    if confidence <= 0 or confidence >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    for i, array in enumerate(data):
        print("系列{}".format(i + 1))
        length, sample_mean, sample_variance, _ = describe(array)
        prompt.prompt_interval_estimate(
            length, sample_mean, sample_variance, pop_variance, confidence)
        print()


@cmd.command()
@click.option("-n", type=int, default=0, help="データの大きさ")
@click.option("-h", "--hypothesis", type=float, default=0, help="帰無仮説で等しいと仮定する平均")
@click.option("-m", "--mean", type=float, default=0, help="標本平均")
@click.option("-p", "--pop_variance", type=float, default=0, help="既知の母分散")
@click.option("-c", "--significance", type=float, default=0.95, help="有意水準(default: 0.95)")
@click.option("-s", "--side", type=click.Choice(["double", "left", "right"]), default="double", help="検定方法(両側，左片側，右片側")
def test(n: int, hypothesis: float, mean: float, pop_variance: float, significance: float, side: str):
    if significance <= 0 or significance >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()

    (is_reject, test_stat) = stats_test.test_mean_with_pop_variance(
        n, hypothesis, mean, pop_variance, significance, side_from_str(side))
    if is_reject:
        print("帰無仮説 'μ = {}' は棄却されました{}".format(hypothesis, test_stat))
    else:
        print("帰無仮説 'μ = {}' は採択されました{}".format(hypothesis, test_stat))


def side_from_str(side: str) -> stats_test.Side:
    if side == "double":
        return stats_test.Side.DOUBLE
    elif side == "left":
        return stats_test.Side.LEFT
    elif side == "right":
        return stats_test.Side.RIGHT
    else:
        return None


def main():
    cmd(obj={})


if __name__ == "__main__":
    main()
