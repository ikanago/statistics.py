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
        contents = [[float(v) for v in row] for row in reader]
        data = np.array(contents[0])
        ctx.obj["data"] = data


@cmd.command()
@click.pass_context
def desc(ctx):
    data = ctx.obj["data"]
    prompt.prompt_describe(data)


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
    sample_mean, sample_variance, _ = describe(data)
    prompt.prompt_interval_estimate(
        sample_mean, sample_variance, pop_variance, confidence, len(data))


def main():
    cmd(obj={})


if __name__ == "__main__":
    main()
