import numpy as np


def describe(data: np.ndarray) -> (float, float, float):
    """
    データの基本的な統計量を求める．

    ## Parameters

    `data`: 対象データ

    ## Returns

    (`sample_mean`, `sample_variance`, `unbiased_variance`):

        データの標本平均，標本分散，不偏分散
    """
    sample_mean = data.mean()
    sample_variance = data.var()
    unbiased_variance = data.var(ddof=1)
    return (sample_mean, sample_variance, unbiased_variance)
