import collections
import json
from pymongo import MongoClient
import urllib
import progressbar
import re
import numpy as np
import pandas as pd

if __name__ == "__main__":

    print("Starting...")

    password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
    client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

    # connect to PTT corpus
    db = client['PTT']

    #  ----- list out all the board names in PTT corpus ----- #
    # ['AllTogether', 'Baseball', 'Boy-Girl'...]
    board_list = db.collection_names()

    board_freq_dict = {}

    for board in board_list[:-2]: # loop over all boards while avoiding 'system.index' and 'system.users'
        collect = db[board]
        print("Currently processing {} board...".format(board))

        p_bar = 1  # set the progressbar to start at one
        post_count = 0
        with progressbar.ProgressBar(max_value=progressbar.UnknownLength):

            for post in collect.find():
                post_count += 1
                p_bar += 1

        print("Writing {} to dictionary...".format(board))
        board_freq_dict[board] = post_count

    board_mean = np.mean(list(board_freq_dict.values()))
    board_std = np.std(list(board_freq_dict.values()))

    board_freq_dict['board_mean'] = board_mean
    board_freq_dict['board_std'] = board_std

    df = pd.DataFrame(board_freq_dict, index=[0])

    df.to_csv("board_freq.csv", encoding='utf8', index=False)

    with open("board_freq.json", 'w', encoding='utf8') as json_file:
        json.dump(board_freq_dict, json_file, ensure_ascii=False)
