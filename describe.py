import csv
import click
import numpy as np


def describe(data: list) -> (int, float, float, float):
    """
    標本の基本的な統計量を求める．

    ## Parameters

    `data`: 対象標本

    ## Returns

    (`length`, `sample_mean`, `sample_variance`, `unbiased_variance`):

        標本の大きさ，標本平均，標本分散，不偏分散
    """
    data = np.array(data)
    sample_mean = data.mean()
    sample_variance = data.var()
    unbiased_variance = data.var(ddof=1)
    return (len(data), sample_mean, sample_variance, unbiased_variance)


@click.command()
@click.option("-f", "--file", type=click.Path(exists=True), default="data.csv")
def cmd(file):
    with open(file) as f:
        reader = csv.reader(f)
        # 2-dimensional array, but each row can be different number of elements.
        contents = [[float(v) for v in row] for row in reader]
        for i, row in enumerate(contents):
            length, sample_mean, sample_variance, unbiased_variance = describe(
                row)
            print("系列{}".format(i + 1))
            print("標本数: {}".format(length))
            print("標本平均: {}".format(sample_mean))
            print("標本分散: {}".format(sample_variance))
            print("不偏分散: {}\n".format(unbiased_variance))


def main():
    cmd()


if __name__ == "__main__":
    main()
