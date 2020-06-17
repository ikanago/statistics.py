from scipy import stats
import numpy as np
import math

def interval_estimate_mean_with_pop_variance(sample_mean: float, pop_varianse: float, n: int):
    normarized_varianse = math.sqrt(pop_varianse / n)
    bottom, top = stats.norm.interval(0.95, loc=sample_mean, scale=normarized_varianse)
    return (bottom, top)

def main():
    data = np.array([100, 70, 30, 60, 50])
    data_size = len(data)
    sample_mean = data.mean()
    sample_variance = data.var()
    unbiased_variance = sample_variance * data_size / (data_size - 1)
    print("標本平均: ", sample_mean)
    print("標本分散: ", sample_variance)
    print("不偏分散: ", unbiased_variance)

    pop_variance = 625
    bottom, top = interval_estimate_mean_with_pop_variance(sample_mean, pop_variance, data_size)
    print("母平均の95%信頼区間(母分散既知): [", bottom, ", ", top, "]")

if __name__ == "__main__":
    main()
