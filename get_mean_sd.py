import json
import numpy as np
import argparse

"""
This program calculates the mean and standard deviation of a token or a list of tokens.
"""


def mean_and_sd(token, json_file):
    """
    Search for word in frequency_dict; if found, append the corresponding number to totals list, else return zero;
    then convert list to numpy array to calculate mean and standard deviation; 
    finally, return mean and standard deviation.
    :param token: Get the mean and standard deviation for this token.
    :param json_file: A json file that contains a frequency distribution dictionary.
    :return: Returns that mean and standard deviation for a token.
    """
    with open(json_file, encoding='utf8') as data_file:

        freq_dict_json = json.load(data_file)  # load freq_dict from json file

        totals = []

        for board in freq_dict_json:  # searches through each board key
            freq = freq_dict_json[board].get(token, 0)  # if found, get frequency from board; else return "0"
            totals.append(freq)  # if word is found, the corresponding number is appended to list
            if freq == 1:
                print("Found {:>4} instance in {}".format(freq, board))  # diagnostic
            else:
                print("Found {:>4} instances in {}".format(freq, board))  # diagnostic

        totals_array = np.array(totals)  # convert list to numpy array for easier computation
        print("Total found: {}".format(np.sum(totals_array)))  # diagnostic

        mean = np.mean(totals_array)  # calculate mean
        standard_deviation = np.std(totals_array)  # calculate standard deviation
        # print("Mean is {}, standard deviation is {}".format(mean, standard_deviation))  # diagnostic

    return mean, standard_deviation


def print_results(token, mean, standard_deviation, **kwargs):
    """
    Prints the token, mean, and standard deviation calculated from mean_and_sd. If input file is provided, results
    are saved to output.txt file.
    :param token: The token that was processed by mean_and_sd
    :param mean: The mean calculated by mean_and_sd.
    :param standard_deviation: The standard deviation calculated by mean_and_sd.
    :param kwargs: Pass additional print arguments to the print function.
    :return: Returns nothing.
    """
    if args.quiet:
        print("{}, {}, {}".format(token, mean, standard_deviation), **kwargs)
    elif args.verbose:
        print("{}: the mean is {}; the sd is {}".format(token, mean, standard_deviation), **kwargs)
    else:
        print("Mean is {}, sd is {}".format(mean, standard_deviation), **kwargs)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="This program calculates the mean and standard deviation of a token"
                                                 " or a group of tokens. Output format is: mean, sd")
    group = parser.add_mutually_exclusive_group()
    token_group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("freq_dict", help="A json file containing frequency distributions for tokens.")
    # parser.add_argument("token", nargs="+", help="One or more tokens")
    token_group.add_argument("-t", "--token", nargs="*", help="One or more tokens.")
    token_group.add_argument("-file", "--token_file", help="A file containing tokens.",
                             type=argparse.FileType('r', encoding='utf8'))
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    if args.token_file:
        with open("output.txt", 'w', encoding="utf8") as output:
            print("token, mean, sd", file=output)
            for arg in args.token_file.readlines()[1:]:  # strange character appearing in the first line
                mean_num, sd_num = mean_and_sd(arg.strip(), args.freq_dict)
                print_results(arg.strip(), mean_num, sd_num, file=output)
    else:
        for arg in args.token:
            mean_num, sd_num = mean_and_sd(arg, args.freq_dict)
            print_results(arg, mean_num, sd_num)
    # else:
    #
    #     mean_num, sd_num = mean_and_sd(args.token, args.freq_dict)
    #
    #     if args.quiet:
    #         print(mean_num, sd_num)
    #     elif args.verbose:
    #         print("{}: the mean is {}; the standard deviation is {}".format(args.token, mean_num, sd_num))
    #     else:
    #         print("Mean is {}, standard deviation is {}".format(mean_num, sd_num))
