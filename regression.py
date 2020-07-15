import click
import csv
from scipy import stats
import math


@click.command()
@click.option("-f", "--file", type=click.Path(exists=True), default="data.csv")
def cmd(file):
    with open(file) as f:
        reader = csv.reader(f)
        # 2-dimensional array, but each row can be different number of elements.
        contents = [[float(v) for v in row] for row in reader]
        if len(contents) < 2:
            print("回帰分析には2つの系列のデータが必要です．")
            exit()
        if len(contents[0]) != len(contents[1]):
            print("2つの系列のデータの大きさが異なります．")
            exit()

        correl, _ = stats.pearsonr(contents[0], contents[1])
        b, a, _, _, _ = stats.linregress(contents[0], contents[1])
        print("相関係数: {}\n標本回帰直線: y = {}x + {}".format(correl, b, a))


def main():
    cmd()


if __name__ == "__main__":
    main()
