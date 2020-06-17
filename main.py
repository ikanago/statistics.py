from scipy import stats
import numpy as np
import math

def normarize_variance(variance: float, n: int):
    return math.sqrt(variance / n)

def interval_estimate_mean_with_pop_variance(sample_mean: float, pop_varianse: float, n: int):
    normarized_varianse = normarize_variance(pop_varianse, n)
    bottom, up = stats.norm.interval(0.95, loc=sample_mean, scale=normarized_varianse)
    return (bottom, up)

def interval_estimate_mean_without_pop_variance(sample_mean: float, sample_varianse: float, n: int):
    degree_of_freedom = n - 1
    normarized_variance = normarize_variance(sample_varianse, degree_of_freedom)
    bottom, up = stats.t.interval(0.95, loc=sample_mean, scale=normarized_variance, df=degree_of_freedom)
    return (bottom, up)

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
    bottom, up = interval_estimate_mean_with_pop_variance(sample_mean, pop_variance, data_size)
    print("母平均の95%信頼区間(母分散既知): [", bottom, ", ", up, "]")

    bottom, up = interval_estimate_mean_without_pop_variance(sample_mean, sample_variance, data_size)
    print("母平均の95%信頼区間(母平均未知): [ {}, {} ]".format(bottom, up))

if __name__ == "__main__":
    main()
