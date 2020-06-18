import argparse
import csv

import numpy as np

import interval_estimation
import prompt
from describe import describe


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    parser_desc = subparsers.add_parser("desc")
    parser_est = subparsers.add_parser("est")
    parser.add_argument("-i", "--input", type=str, default="data.csv",
                        help="入力データの記録されたCSVファイルへのパス(default: data.csv).")
    parser_est.add_argument("-c", "--confidence", type=float,
                            default=0.95, help="信頼係数(default: 0.95)")
    parser_est.add_argument("-p", "--pop_variance", type=float,
                            default=0, help="既知の母分散")
    args = parser.parse_args()
    command = args.subparser_name
    input_file = args.input

    with open(input_file) as f:
        reader = csv.reader(f)
        contents = [[float(v) for v in row] for row in reader]
        data = np.array(contents[0])

    if command == "desc":
        prompt.prompt_describe(data)
    elif command == "est":
        confidence = args.confidence
        pop_variance = args.pop_variance
        if confidence <= 0 or confidence >= 1:
            import sys
            print("信頼係数は(0, 1)の範囲で指定してください．", file=sys.stderr)
            exit()

        sample_mean, sample_variance, _ = describe(data)
        prompt.prompt_interval_estimate(
            sample_mean, sample_variance, pop_variance, confidence, len(data))


if __name__ == "__main__":
    main()
