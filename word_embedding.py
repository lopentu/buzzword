import pymongo
from pymongo import MongoClient
import urllib, re, json
import jieba
import gensim
import logging
import pickle

# ----- login db ----- #
password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

# ----- connect to PTT corpus ----- #
db = client['PTT']

# ----- extract all board names ----- #
# board_list = db.collection_names() 
# print(board_list)

# ----- access all boards ----- #
AllTogether = db['AllTogether']
Baseball = db['Baseball']
Beauty = db['Beauty']
Boy_Girl = db['Boy-Girl']
BuyTogether = db['BuyTogether']
ChangHua = db['ChangHua']
Chiayi = db['Chiayi']
ChungLi = db['ChungLi']
Daliao = db['Daliao']
FengYuan = db['FengYuan']
FongShan = db['FongShan']
Food = db['Food']
FuMouDiscuss = db['FuMouDiscuss']
Gossiping = db['Gossiping']
Hate = db['Hate']
Hsinchu = db['Hsinchu']
Hualien = db['Hualien']
I_Lan = db['I-Lan']
Jinmen = db['Jinmen']
Kaohsiung = db['Kaohsiung']
Keelung = db['Keelung']
Linyuan = db['Linyuan']
LoL = db['LoL']
Matsu = db['Matsu']
MenTalk = db['MenTalk']
Miaoli = db['Miaoli']
NBA = db['NBA']
Nantou = db['Nantou']
PH_sea = db['PH-sea']
PingTung = db['PingTung']
PuzzleDragon = db['PuzzleDragon']
Sad = db['Sad']
Stock = db['Stock']
StupidClown = db['StupidClown']
TaichungBun = db['TaichungBun']
TaichungCont = db['TaichungCont']
Tainan = db['Tainan']
Taitung = db['Taitung']
Taoyuan = db['Taoyuan']
ToS = db['ToS']
WomenTalk = db['WomenTalk']
Yunlin = db['Yunlin']
ask = db['ask']
happy = db['happy']
home_sale = db['home-sale']
iPhone = db['iPhone']
joke = db['joke']
movie = db['movie']
prozac = db['prozac']

ptt_posts = []

# --- set ref corpus --- #
test_data = zip(AllTogether.find()[:100], Baseball.find()[:100], Beauty.find()[:100], Boy_Girl.find()[:100]\
				, BuyTogether.find()[:100], ChangHua.find()[:100], Chiayi.find()[:100], ChungLi.find()[:100]\
				, Daliao.find()[:100], FengYuan.find()[:100], FongShan.find()[:100], Food.find()[:100]\
				, FuMouDiscuss.find()[:100], Gossiping.find()[:5000], Hate.find()[:100], Hsinchu.find()[:100]\
				, Hualien.find()[:100], I_Lan.find()[:100], Jinmen.find()[:100], Kaohsiung.find()[:100]\
				, Keelung.find()[:100], Linyuan.find()[:100], LoL.find()[:100], Matsu.find()[:100]\
				, MenTalk.find()[:100], Miaoli.find()[:100], NBA.find()[:100], Nantou.find()[:100]\
				, PH_sea.find()[:100], PingTung.find()[:100], PuzzleDragon.find()[:100], Sad.find()[:100]\
				, Stock.find()[:100], StupidClown.find()[:100], TaichungBun.find()[:100], TaichungCont.find()[:100]\
				, Tainan.find()[:100], Taitung.find()[:100], Taoyuan.find()[:100], ToS.find()[:100]\
				, WomenTalk.find()[:100], Yunlin.find()[:100], ask.find()[:100], happy.find()[:100]\
				, home_sale.find()[:100], iPhone.find()[:100], joke.find()[:100], movie.find()[:100]\
				, prozac.find()[:100])

punctuations = '\n|\?|\？|\.|。|，|\^|\s|=|、|！|\!|\/|\／|\）|\(|\）|>|<|"||\「|\」|\:|\◎|\☆|\Σ|\-|~|˙|→|一|____________________________|'

for content in test_data:
	for nums in [position for position, article in enumerate(content)]:
		jieba.load_userdict('aged.lexicon/target.test.txt') # seg by test word list
		clean_content = re.sub(punctuations,'', content[nums]['content'])
		word = jieba.cut(clean_content, cut_all=False)
		ptt_posts.append([i for i in word])
# print(ptt_posts)

# --- train word embedding --- #
model = gensim.models.Word2Vec(ptt_posts, min_count=1)  # min_count 低頻詞 / worker 工作環境 / window 上下文 / size vector的數量

filename = 'word_embedding_model.sav'
pickle.dump(model, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))


# --- view trained result --- #
# print(loaded_model.wv['比賽'])  # examine array of target word
print(loaded_model.wv.most_similar(positive = ['辣妹'])) # find the top relevant words to target word
#print(loaded_model.wv.most_similar(positive = ['比賽','看'])) # find the top relevant words to both of the target words
#print(loaded_model.wv.similarity('比賽', '看')) # find the distance of the two words










































