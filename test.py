import pymongo
from pymongo import MongoClient
import urllib, re, json
import jieba
import gensim
import logging

# ----- login db ----- #
password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
print(password)
client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

# ----- connect to PTT corpus ----- #
db = client['PTT']

#  ----- access a board ----- #
# collect = db['Baseball']

# ----- extract all board names ----- #
# board_list = db.collection_names() 
# print(board_list)

# ----- access boards ----- #

''' ['AllTogether', 'Baseball', 'Beauty', 'Boy-Girl', 'BuyTogether', 'ChangHua', 'Chiayi', 
'ChungLi', 'Daliao', 'FengYuan', 'FongShan', 'Food', 'FuMouDiscuss', 'Gossiping', 'Hate', 
'Hsinchu', 'Hualien', 'I-Lan', 'Jinmen', 'Kaohsiung', 'Keelung', 'Linyuan', 'LoL', 'Matsu',
 'MenTalk', 'Miaoli', 'NBA', 'Nantou', 'PH-sea', 'PingTung', 'PuzzleDragon', 'Sad', 'Stock',
 'StupidClown', 'TaichungBun', 'TaichungCont', 'Tainan', 'Taitung', 'Taoyuan', 'ToS', 'WomenTalk',
 'Yunlin', 'ask', 'happy', 'home-sale', 'iPhone', 'joke', 'movie', 'prozac', 'system.indexes', 'system.users'] '''

AllTogether = db['AllTogether']
Baseball = db['Baseball']
# Beauty = db['Beauty']
# Boy_Girl = db['Boy-Girl']
# BuyTogether = db['BuyTogether']
# ChangHua = db['ChangHua']
# Chiayi = db['Chiayi']
# ChungLi = db['ChungLi']
# Daliao = db['Daliao']
# FengYuan = db['FengYuan']
# FongShan = db['FongShan']
# Food = db['Food']
# FuMouDiscuss = db['FuMouDiscuss']
# Gossiping = db['Gossiping']
# Hate = db['Hate']
# Hsinchu = db['Hsinchu']
# Hualien = db['Hualien']
# I_Lan = db['I-Lan']
# Jinmen = db['Jinmen']
# Kaohsiung = db['Kaohsiung']
# Keelung = db['Keelung']
# Linyuan = db['Linyuan']
# LoL = db['LoL']
# Matsu = db['Matsu']
# MenTalk = db['MenTalk']
# Miaoli = db['Miaoli']
# NBA = db['NBA']
# Nantou = db['Nantou']
# PH_sea = db['PH-sea']
# PingTung = db['PingTung']
# PuzzleDragon = db['PuzzleDragon']
# Sad = db['Sad']
# Stock = db['Stock']
# StupidClown = db['StupidClown']
# TaichungBun = db['TaichungBun']
# TaichungCont = db['TaichungCont']
# Tainan = db['Tainan']
# Taitung = db['Taitung']
# Taoyuan = db['Taoyuan']
# ToS = db['ToS']
# WomenTalk = db['WomenTalk']
# Yunlin = db['Yunlin']
# ask = db['ask']
# happy = db['happy']
# home_sale = db['home-sale']
# iPhone = db['iPhone']
# joke = db['joke']
# movie = db['movie']
# prozac = db['prozac']

ptt_posts = []
for content in AllTogether.find()[:10]:
	clean_content = re.sub('\n|\?|\？|\.|。|，|\^|\s|=|、|！|\!|\/|（|）|(|)|「|」|\~|\:','', content['content'])
	word = jieba.cut(clean_content, cut_all=False)
	ptt_posts.append([i for i in word])
print(ptt_posts)
	# ptt_posts.append(clean_content)
	# ptt_posts.append(content['content'])  # 斷詞、清標點、list 
# print(ptt_posts)








































