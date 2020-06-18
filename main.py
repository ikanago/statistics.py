import argparse
import csv

import click
import numpy as np

import interval_estimation
import prompt
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


def main():
    cmd(obj={})


if __name__ == "__main__":
    main()
