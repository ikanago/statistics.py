import argparse
import csv
import numpy as np
import interval_estimation


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default="data.csv",
                        help="入力データの記録されたCSVファイルへのパス(default: data.csv).")
    parser.add_argument("-c", "--confidence", type=float,
                        default=0.95, help="信頼係数(default: 0.95)")
    parser.add_argument("-p", "--pop_variance", type=float, default=0, help="既知の母分散")
    args = parser.parse_args()
    input_file = args.input
    confidence = args.confidence
    pop_variance = args.pop_variance
    if confidence <= 0 or confidence >= 1:
        import sys
        print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
        exit()
    if pop_variance <= 0:
        import sys
        print("母分散既知の母平均の区間推定はできません．", file=sys.stderr)

    with open(input_file) as f:
        reader = csv.reader(f)
        contents = [[float(v) for v in row] for row in reader]
        data = np.array(contents[0])

    data_size = len(data)
    sample_mean, sample_variance, unbiased_variance = describe(data)
    print("データ数: {}".format(data_size))
    print("標本平均: {}".format(sample_mean))
    print("標本分散: {}".format(sample_variance))
    print("不偏分散: {}".format(unbiased_variance))

    bottom, top = interval_estimation.interval_estimate_mean_with_pop_variance(
        sample_mean, pop_variance, data_size, confidence)
    print("母平均の{}%信頼区間(母分散既知): [ {}, {} ]".format(int(confidence * 100), bottom, top))

    bottom, top = interval_estimation.interval_estimate_mean_without_pop_variance(
        sample_mean, sample_variance, data_size, confidence)
    print("母平均の{}%信頼区間(母分散未知): [ {}, {} ]".format(int(confidence * 100), bottom, top))

    bottom, top = interval_estimation.interval_estimate_variance(
        sample_variance, data_size, confidence)
    print("母分散の{}%信頼区間            : [ {}, {} ]".format(int(confidence * 100), bottom, top))


if __name__ == "__main__":
    main()
