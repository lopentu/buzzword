import collections
import json
from pymongo import MongoClient
import urllib
import progressbar
import re

"""
This program creates:
1. a file with raw posts from each PTT board,
2. a frequency list for each token found in PTT that is then saved to a json file
"""


def recursive_dict():
    """
    Recursively calls itself to create a nested dictionary with as many layers as needed.
    :return: Returns a collections.defaultdict object that creates itself. 
    """
    return collections.defaultdict(recursive_dict)


def create_posts_dict_and_write_raw_posts_to_file():
    """
    Create a nested dictionary with this structure: {"board_name": {"year": {"month": [posts] } } }. Also creates a
    text file with raw posts to be used as input to the parser. 
    :return: Returns a dictionary with board names as keys and words from that board as values.
    """

    regex = re.compile(r'(.+)-(.+)-(.+)')  # create a regex to capture the year and month of a post
#    num_posts_to_collect = 100  # select the number of posts to collect for each board

    for board in board_list[:-2]:  # loop over all boards while avoiding 'system.index' and 'system.users'
        # initialize a defaultdict
        time_board_dict = recursive_dict()
        collect = db[board]  # 49 boards altogether
        print("Currently processing {} board...".format(board))

        p_bar = 1  # set the progressbar to start at one

        with open("raw/{}_raw.txt".format(board), "w", encoding="utf8") as raw_file:

            with progressbar.ProgressBar(max_value=progressbar.UnknownLength) as bar:

                for post in collect.find():  # choose number of posts to collect

                    date = regex.search(str(post['post_time']))
                    year = date.group(1)
                    month = date.group(2)

                    bar.update(p_bar)
                    p_bar += 1

                    print(post['content'], file=raw_file)  # write raw posts to file

                    for seg in post['content_seg']:  # select already tokenized and parsed content i.e. [token, POS]
                        # seg[1] checks POS; filter out non-words; add 'Neu' to filter numbers
                        if seg[1] not in ['LINEBREAK', 'PUNCTUATION', 'caa']:
                            if time_board_dict[board][year][month]:  # if a list already exists, append
                                time_board_dict[board][year][month].append(seg[0])
                            else:  # otherwise, create a new list with the token as the first item
                                time_board_dict[board][year][month] = [seg[0]]

        frequency_dict = recursive_dict()
        print("Creating {} frequency list...".format(board))

        for board_name in time_board_dict:
            for year in time_board_dict[board_name]:
                for month in time_board_dict[board_name][year]:
                    frequency_dict[board][year][month] = collections.Counter(time_board_dict[board_name][year][month])

        with open("freq/{}_freq_dict.json".format(board), "w", encoding="utf8") as freq_dict_json:
            print("Writing to json file...")
            # save freq_dict to json file for future use
            json.dump(frequency_dict, freq_dict_json, indent=4, ensure_ascii=False)


# def create_freq_dict_and_write_dict_to_file(time_board_dict):
#     """
#     Create a frequency dictionary with board names as keys and a collections.Counter objects as values; also write
#     dictionary to json file for later use.
#     :param time_board_dict: A Python dictionary containing PTT board names as keys and a list of words for that
#                             board as values.
#     :return: Returns a dictionary with board names as keys and a collections.Counter object as its value.
#     """
#     frequency_dict = recursive_dict()
#
#     for board in time_board_dict:
#         for year in time_board_dict[board]:
#             for month in time_board_dict[board][year]:
#                 frequency_dict[board][year][month] = collections.Counter(time_board_dict[board][year][month])
#
#     with open("freq_dict.json", "w", encoding="utf8") as freq_dict_json:
#
#         # save freq_dict to json file for future use
#         json.dump(frequency_dict, freq_dict_json, indent=4, ensure_ascii=False)
#
#     return frequency_dict


if __name__ == "__main__":

    print("Starting...")

    password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
    client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

    # connect to PTT corpus
    db = client['PTT']

    #  ----- list out all the board names in PTT corpus ----- #
    # ['AllTogether', 'Baseball', 'Boy-Girl'...]
    board_list = db.collection_names()

    create_posts_dict_and_write_raw_posts_to_file()

    # create_freq_dict_and_write_dict_to_file(posts_dict)

    print("Raw text and json file created.")
