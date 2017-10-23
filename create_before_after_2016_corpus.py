from pymongo import MongoClient
import urllib
import progressbar
import re
import pandas as pd

"""
This program creates:
1. a file with raw posts from each PTT board, divided between after 2016 posts and before 2016 posts,
"""


def create_split_corpus():
    """
    Create a nested dictionary with this structure: {"board_name": {"year": {"month": [posts] } } }. Also creates a
    text file with raw posts to be used as input to the parser.
    :return: nothing.
    """

    regex = re.compile(r'(.+)-(.+)-(.+)')  # create a regex to capture the year and month of a post
    # num_posts_to_collect = 100  # select the number of posts to collect for each board
    years = ['2016', '2017']

    df = pd.read_table("aged.lexicon/target.test.txt", encoding='utf8', names=['token', 'type'])

    for board in board_list[:-2]:  # loop over all boards while avoiding 'system.index' and 'system.users'
        collect = db[board]  # 49 boards altogether
        print("Currently processing {} board...".format(board))

        p_bar = 1  # set the progressbar to start at one

        with open("raw_split/{}_raw_after_2016.txt".format(board), "w", encoding="utf8") as after_2016_file,\
                open("raw_split/{}_raw_before_2016.txt".format(board), "w", encoding="utf8") as before_2016_file:

            with progressbar.ProgressBar(max_value=progressbar.UnknownLength) as bar:

                for post in collect.find():  # choose number of posts to collect
                    bar.update(p_bar)
                    p_bar += 1

                    for buzzword in df['token'].values:
                        if buzzword in post['content']:

                            date = regex.search(str(post['post_time']))
                            year = date.group(1)
                            month = date.group(2)

                            if year in years:
                                print(post['content'], file=after_2016_file)  # write posts after 2016 to file
                            else:
                                print(post['content'], file=before_2016_file)  # write posts before 2016 to file


if __name__ == "__main__":

    print("Starting...")

    password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
    client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

    # connect to PTT corpus
    db = client['PTT']

    #  ----- list out all the board names in PTT corpus ----- #
    # ['AllTogether', 'Baseball', 'Boy-Girl'...]
    board_list = db.collection_names()

    create_split_corpus()

    print("Split corpus created.")
