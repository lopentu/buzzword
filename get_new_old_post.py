import pymongo
from pymongo import MongoClient
import urllib
import datetime
import pandas as pd
import json
from bson import json_util


oldest_time = {"Oldest_Date": datetime.datetime.now(), "Board_Name": 'board_name', "Post": 'post'}
newest_time = {"Newest_Date": datetime.datetime(1, 1, 1), "Board_Name": 'board_name', "Post": 'post'}

print("Starting...")

password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

# connect to PTT corpus
db = client['PTT']

#  ----- list out all the board names in PTT corpus ----- #
# ['AllTogether', 'Baseball', 'Boy-Girl'...]
board_list = db.collection_names()

for board in board_list[:-2]:
    print("Checking {}...".format(board))
    collect = db[board]

    for post in collect.find()[:10]:
        current_post_time = post['post_time']

        if current_post_time > newest_time["Newest_Date"]:
            newest_time["Newest_Date"] = current_post_time
            newest_time["Board_Name"] = board
            newest_time["Post"] = post['content']
        if current_post_time < oldest_time["Oldest_Date"]:
            oldest_time["Oldest_Date"] = current_post_time
            oldest_time["Board_Name"] = board
            oldest_time["Post"] = post['content']

print(oldest_time)
print(newest_time)

time_list = [oldest_time, newest_time]

df = pd.DataFrame(time_list)
df.to_csv("newest_oldest_post.csv", encoding='utf8', index=False)

with open("newest_oldest_post.json", 'w', encoding='utf8') as json_file:
    json.dump(time_list, json_file, ensure_ascii=False, default=json_util.default)
