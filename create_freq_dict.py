import collections
import json
from pymongo import MongoClient
import urllib
import progressbar

"""
This program creates:
1. a file with raw posts from each PTT board,
2. a frequency list for each token found in PTT that is then saved to a json file
"""


def create_posts_dict_and_write_raw_posts_to_file():
    """
    Create a dictionary with board names as keys and a list of words from that board as values; also create a text file 
    with raw posts to be used as input to the parser. 
    :return: Returns a dictionary with board names as keys and words from that board as values.
    """
    # initialize defaultdict; an empty list is generated the first time a key is encountered
    posts_dictionary = collections.defaultdict(list)

    num_posts_to_collect = 100
    p_bar = 1

    with open("sent_from_boards.txt", "w", encoding="utf8") as sent_from_boards_file:
        with progressbar.ProgressBar(max_value=num_posts_to_collect * 49) as bar:

            for board in board_list[:-2]:  # loop over all boards while avoiding 'system.index' and 'system.users'
                collect = db[board]  # 49 boards altogether
                for post in collect.find()[:num_posts_to_collect]:  # choose number of posts to collect
                    bar.update(p_bar)
                    p_bar += 1
                    print(post['content'], file=sent_from_boards_file)  # write raw posts to file

                    for seg in post['content_seg']:  # select already tokenized and parsed content i.e. [token, POS]
                        # seg[1] checks POS; filter out non-words; add 'Neu' to filter numbers
                        if seg[1] not in ['LINEBREAK', 'PUNCTUATION', 'caa']:
                            posts_dictionary[board].append(seg[0])  # append the token to the current board's list

    return posts_dictionary


def create_freq_dict_and_write_dict_to_file(posts_dictionary):
    """
    Create a frequency dictionary with board names as keys and a collections.Counter objects as values; also write 
    dictionary to json file for later use.
    :param posts_dictionary: A Python dictionary containing PTT board names as keys and a list of words for that 
                            board as values.
    :return: Returns a dictionary with board names as keys and a collections.Counter object as its value.
    """
    frequency_dict = {}

    for board in posts_dictionary:  # for each board in posts_dict
        # the key of post_dict, i.e. "board", is used as key for frequency_dict;
        # a Counter object is used as a value to that key
        frequency_dict[board] = collections.Counter(posts_dictionary[board])

    with open("freq_dict.json", "w", encoding="utf8") as freq_dict_json:

        # save freq_dict to json file for future use
        json.dump(frequency_dict, freq_dict_json, indent=4, ensure_ascii=False)

    return frequency_dict


if __name__ == "__main__":

    print("Starting...")

    password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
    client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

    # connect to PTT corpus
    db = client['PTT'] 

    #  ----- list out all the board names in PTT corpus ----- #
    # ['AllTogether', 'Baseball', 'Boy-Girl'...]
    board_list = db.collection_names() 

    print("Collecting posts and writing raw text to file...")

    posts_dict = create_posts_dict_and_write_raw_posts_to_file()

    print("Creating freq list and writing to json file...")

    create_freq_dict_and_write_dict_to_file(posts_dict)

    print("Raw text and json file created.")
