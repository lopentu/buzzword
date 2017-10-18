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
test_data = zip(AllTogether.find()[:], Baseball.find()[:], Beauty.find()[:], Boy_Girl.find()[:]\
				, BuyTogether.find()[:], ChangHua.find()[:], Chiayi.find()[:], ChungLi.find()[:]\
				, Daliao.find()[:], FengYuan.find()[:], FongShan.find()[:], Food.find()[:]\
				, FuMouDiscuss.find()[:], Gossiping.find()[:], Hate.find()[:], Hsinchu.find()[:]\
				, Hualien.find()[:], I_Lan.find()[:], Jinmen.find()[:], Kaohsiung.find()[:]\
				, Keelung.find()[:], Linyuan.find()[:], LoL.find()[:], Matsu.find()[:]\
				, MenTalk.find()[:], Miaoli.find()[:], NBA.find()[:], Nantou.find()[:]\
				, PH_sea.find()[:], PingTung.find()[:], PuzzleDragon.find()[:], Sad.find()[:]\
				, Stock.find()[:], StupidClown.find()[:], TaichungBun.find()[:], TaichungCont.find()[:]\
				, Tainan.find()[:], Taitung.find()[:], Taoyuan.find()[:], ToS.find()[:]\
				, WomenTalk.find()[:], Yunlin.find()[:], ask.find()[:], happy.find()[:]\
				, home_sale.find()[:], iPhone.find()[:], joke.find()[:], movie.find()[:]\
				, prozac.find()[:])

punctuations = '\n|\?|\？|\.|。|，|\^|\s|=|、|！|\!|\/|\／|\）|\(|\）|>|<|"||\「|\」|\:|\◎|\☆|\Σ|\-|~|˙|→|一|____________________________|'

for content in test_data:
	for nums in [position for position, article in enumerate(content)]:
		stopword = open('stopword.txt','r', encoding='utf8').read()
		jieba.load_userdict('aged.lexicon/target.test.txt') # seg by test word list
		clean_content = re.sub(punctuations,'', content[nums]['content'])
		word = jieba.cut(clean_content, cut_all=False)
		ptt_posts.append([i for i in word if i not in stopword])
# print(ptt_posts)

# --- train word embedding --- #
# model = gensim.models.Word2Vec(ptt_posts, min_count=1)  
model = gensim.models.word2vec.Word2Vec(sentences= ptt_posts, size=100, alpha=0.025, window=10, min_count=5,\
		 max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5,\
		 cbow_mean=1, iter=5, null_word=0, trim_rule=None, sorted_vocab=1,\
		 batch_words=10000)

# --- write training result as python pickle file --- #
filename = 'word_embedding_model.sav'
pickle.dump(model, open(filename, 'wb'))

# --- load the model from pickle --- #
# loaded_model = pickle.load(open(filename, 'rb'))


# --- view trained result --- #
# print(loaded_model.wv['比賽'])  # examine array of target word
# print(loaded_model.wv.most_similar(positive = ['正妹'])) # find the top relevant words to target word
# print(loaded_model.wv.most_similar(positive = ['比賽','看'])) # find the top relevant words to both of the target words
# print(loaded_model.wv.similarity('台灣', '臺灣')) # find the distance of the two words










































