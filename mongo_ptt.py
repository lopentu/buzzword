# -*- coding: utf-8 -*- 

# this file is used for accessing the PTT corpus under 132 server

import pymongo
from pymongo import MongoClient
import urllib, re, json


password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

# connect to PTT corpus
db = client['PTT'] 

#  ----- list out all the board names in PTT corpus ----- #
# ['AllTogether', 'Baseball', 'Boy-Girl'...]
board_list = db.collection_names() 

#  ----- access a board ----- #
collect = db['Baseball']

#  ----- list out only the first 10 posts in each board  ----- #
for post in collect.find()[:10]:
	print (post) # every post is a dictionary

# ----- the keys within the first post ----- #
# ['push_num', 'URL', 'boo_num', 'content_seg', 'comments', 'arrow_num', 'post_time', 'author', '_id', 'content', 'comment_differenceValue', 'title']
print(collect.find()[0].keys())

# ----- accessing the element of the first post ----- #
print(collect.find()[0]['content']) # the content of the post
print(collect.find()[0]['post_time']) # the posting time of the post
