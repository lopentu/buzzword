import json
import collections
import numpy as np
import glob
import pandas as pd
# import argparse

"""
This program calculates the frequency across months, boards, and years for a given token.
"""


def recursive_dict():
    """
    Can be used to create nested dictionaries on the spot.
    :return: A nested defaultdict within a defaultdict within...
    """
    return collections.defaultdict(recursive_dict)


def mean_sd_2016_up(token):
    """
    Search for a token in posts from at least 2016 and then calculate several features.
    :param token: 
    :return: Returns frequency diversity, cross board, cross month, frequency by month, frequency by board,
     and frequency by year.
    """

    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    years = ['2016', '2017']
    board_freq = collections.defaultdict(int)
    month_freq = collections.defaultdict(int)
    year_freq = recursive_dict()

    for filename in glob.glob("freq/*.json"):

        with open(filename, encoding='utf8') as json_data:

            freq = json.load(json_data)

            for board in freq:
                print("Checking ", board, "...")

                for year in years:
                    if year in freq[board]:
                        print("{} found in {}".format(year, board))
                        searching_year = freq[board][year]

                        for month in searching_year:
                            board_freq[board] += searching_year[month].get(token, 0)

                        for month in months:  # look through each month, Jan. through Dec.
                            if month not in searching_year:
                                month_freq[month] += 0
                                if year_freq[year][month]:
                                    year_freq[year][month] += 0
                                else:
                                    year_freq[year][month] = 0
                            else:
                                month_freq[month] += searching_year[month].get(token, 0)
                                if year_freq[year][month]:
                                    year_freq[year][month] += searching_year[month].get(token, 0)
                                else:
                                    year_freq[year][month] = searching_year[month].get(token, 0)
                    else:
                        print("{} not found in {}.".format(year, board))
                        board_freq[board] += 0
                        for month in months:
                            month_freq[month] += 0
                            year_freq[year][month] = 0

    print("2016 board_freq: ", len(board_freq), board_freq.values())
    print("2016 month_freq: ", len(month_freq), month_freq.values())

    by_board_mean = np.mean(list(board_freq.values()))
    by_board_sd = np.std(list(board_freq.values()))

    by_month_mean = np.mean(list(month_freq.values()))
    by_month_sd = np.std(list(month_freq.values()))

    cross_board = by_board_mean/by_board_sd
    cross_month = by_month_mean/by_month_sd
    frequency_diversity = (cross_board * cross_month)

    year_to_board = {}
    print("Year freq: ", year_freq)
    for year in year_freq:
        try:
            year_vector = list(year_freq[year].values())
            print("Year vector for: ", year, year_vector)
            print(type(year_vector))
            year_mean = np.mean(year_vector)
            year_sd = np.std(year_vector)
            cross_year = year_mean/year_sd
            year_to_board[year] = cross_board * cross_year
            print(year_to_board)

        except TypeError:
            print("No occurrences found in any board.")
            # frequency_diversity = "NA"
            # cross_month = "NA"
            # cross_board = "NA"
            # by_board_mean = "NA"
            # by_board_sd = "NA"
            # by_month_mean = "NA"
            # by_month_sd = "NA"
    print("=" * 40)
    print(frequency_diversity, by_board_mean, by_board_sd, by_month_mean, by_month_sd)
    return frequency_diversity, cross_board, cross_month, year_to_board, month_freq, board_freq, year_freq


def mean_sd_2015_below(token):
    """
    Search for word in frequency_dict; if found, append the corresponding number to totals list, else return zero;
    then convert list to numpy array to calculate mean and standard deviation; 
    finally, return mean and standard deviation.
    :param token: Get the mean and standard deviation for this token.
    :return: Returns the mean and standard deviation for a token by month and by year separately.
    """

    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    board_freq = collections.defaultdict(int)
    month_freq = collections.defaultdict(int)
    year_freq = collections.defaultdict(recursive_dict)

    for filename in glob.glob("freq/*.json"):

        with open(filename, encoding='utf8') as data:

            freq = json.load(data)

            for board in freq:
                print("Checking ", board, "...")

                for year in freq[board]:
                    if year not in ['2016', '2017']:
                        print("{} found in {}".format(year, board))
                        searching_year = freq[board][year]

                        for month in searching_year:  # creating board_freq
                            board_freq[board] += searching_year[month].get(token, 0)

                        for month in months:  # look through each month, Jan. through Dec.
                            if month not in searching_year:
                                month_freq[month] += 0
                                if year_freq[year][month]:
                                    year_freq[year][month] += 0
                                else:
                                    year_freq[year][month] = 0
                            else:
                                month_freq[month] += searching_year[month].get(token, 0)
                                if year_freq[year][month]:
                                    year_freq[year][month] += searching_year[month].get(token, 0)
                                else:
                                    year_freq[year][month] = searching_year[month].get(token, 0)

                    else:
                        print("{} not found in {}.".format(year, board))
                        board_freq[board] += 0

                        for month in months:
                            month_freq[month] += 0

    year_freq = collections.OrderedDict(sorted(year_freq.items(), key=lambda x: x[0]))

    print(token, "2015 board_freq: ", len(board_freq), np.sum(list(board_freq.values())), sorted(board_freq.keys()))
    print(token, "2015 month_freq: ", len(month_freq), np.sum(list(month_freq.values())), sorted(month_freq.keys()))
    print(token, "2015 year_freq: ", len(year_freq))

    by_board_mean = np.mean(list(board_freq.values()))
    by_board_sd = np.std(list(board_freq.values()))

    by_month_mean = np.mean(list(month_freq.values()))
    by_month_sd = np.std(list(month_freq.values()))

    cross_board = by_board_mean/by_board_sd
    cross_month = by_month_mean/by_month_sd
    frequency_diversity = (cross_board * cross_month)

    year_to_board = {}
    print("Year freq: ", year_freq)
    
    for year in year_freq:
        try:
            year_vector = list(year_freq[year].values())
            print("Year vector for: ", year, year_vector)
            print(type(year_vector))
            year_mean = np.mean(year_vector)
            year_sd = np.std(year_vector)
            cross_year = year_mean/year_sd
            year_to_board[year] = cross_board * cross_year
            print(year_to_board)

        except TypeError:
            print("No occurrences found in any board.")

    print("=" * 40)
    print(frequency_diversity, by_board_mean, by_board_sd, by_month_mean, by_month_sd)
    return frequency_diversity, cross_board, cross_month, year_to_board, month_freq, board_freq, year_freq


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description="This program calculates the mean and standard deviation of a token"
    #                                              " or a group of tokens. Output format is: mean, sd")
    # group = parser.add_mutually_exclusive_group()
    # token_group = parser.add_mutually_exclusive_group(required=True)
    #
    # token_group.add_argument("-t", "--token", nargs="*", help="One or more tokens.")
    # token_group.add_argument("-file", "--token_file", help="A file containing tokens.",
    #                          type=argparse.FileType('r', encoding='utf8'))
    # group.add_argument("-v", "--verbose", action="store_true")
    # group.add_argument("-q", "--quiet", action="store_true")
    # args = parser.parse_args()

    # if args.token_file:
    #     with open("freq_div.txt", 'w', encoding="utf8") as output:
    #         print("token, cross_board_after_2016, cross_month_after_2016, cross_board_before_2016,"
    #               " cross_month_before_2016, cross_year_before_2016",
    #               file=output)
    #         for arg in args.token_file.readlines()[1:]:  # strange character appearing in the first line
                # before 2016

    buzz_list = []
    buzzwords = recursive_dict()

    data = pd.read_table("aged.lexicon/target.test.txt", names=["token", "class"], encoding='utf8')

    for index, row in data.iterrows():
        arg = row['token']
        class_ = row['class']
        freq_d_2015, cross_b_2015, cross_m_2015, \
            y_to_b_2015, month_freq_2015, board_freq_2015, year_freq_2015 = mean_sd_2015_below(arg.strip())

        freq_d_2016, cross_b_2016, cross_m_2016, y_to_b_2016, month_freq_2016, board_freq_2016,\
            year_freq_2016 = mean_sd_2016_up(arg.strip())

        # create a dictionary entry for each buzzword as key
        buzzwords[arg.strip()]["After_2016"]["frequency_diversity"] = freq_d_2016
        buzzwords[arg.strip()]["After_2016"]["cross_board"] = cross_b_2016
        buzzwords[arg.strip()]["After_2016"]["cross_month"] = cross_m_2016
        buzzwords[arg.strip()]["After_2016"]["year_to_board"] = y_to_b_2016
        buzzwords[arg.strip()]["After_2016"]["by_month_frequency"] = month_freq_2016
        buzzwords[arg.strip()]["After_2016"]["by_board_frequency"] = board_freq_2016
        buzzwords[arg.strip()]["After_2016"]["by_year_frequency"] = year_freq_2016

        buzzwords[arg.strip()]["Before_2016"]["frequency_diversity"] = freq_d_2015
        buzzwords[arg.strip()]["Before_2016"]["cross_board"] = cross_b_2015
        buzzwords[arg.strip()]["Before_2016"]["cross_month"] = cross_m_2015
        buzzwords[arg.strip()]["Before_2016"]["year_to_board"] = y_to_b_2015
        buzzwords[arg.strip()]["Before_2016"]["by_month_frequency"] = month_freq_2015
        buzzwords[arg.strip()]["Before_2016"]["by_board_frequency"] = board_freq_2015
        buzzwords[arg.strip()]["Before_2016"]["by_year_frequency"] = year_freq_2015

        buzzword_dict = collections.OrderedDict()
        buzzword_dict["Token"] = arg.strip()
        buzzword_dict["Class"] = class_
        buzzword_dict["After_2016_Cross_Board"] = cross_b_2015
        buzzword_dict["After_2016_Cross_Month"] = cross_m_2016
        buzzword_dict["Before_2016_Cross_board"] = cross_b_2015
        for year in y_to_b_2015:
            buzzword_dict["{}_to_Board".format(year)] = y_to_b_2015[year]

        buzz_list.append(buzzword_dict)

    df = pd.DataFrame(buzz_list)

    df.to_csv("buzz_df.csv", encoding='utf8', index=False)

    # write meta data to json file
    with open("buzzwords_meta.json", 'w', encoding='utf8') as json_file:
        json.dump(buzzwords, json_file, indent=4, ensure_ascii=False)
