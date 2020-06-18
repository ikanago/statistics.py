import numpy as np


def describe(data: list) -> (int, float, float, float):
    """
    データの基本的な統計量を求める．

    ## Parameters

    `data`: 対象データ

    ## Returns

    (`length`, `sample_mean`, `sample_variance`, `unbiased_variance`):

        データの大きさ，標本平均，標本分散，不偏分散
    """
    data = np.array(data)
    sample_mean = data.mean()
    sample_variance = data.var()
    unbiased_variance = data.var(ddof=1)
    return (len(data), sample_mean, sample_variance, unbiased_variance)
