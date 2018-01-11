import pymongo
from pymongo import MongoClient
import urllib, re, json
import jieba
import gensim
import logging
import pickle
from itertools import chain

# # ----- login db ----- #
password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

# # ----- connect to PTT corpus ----- #
db = client['PTT']

# # ----- extract all board names ----- #
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


ptt_boards = [AllTogether, Baseball, Beauty, Boy_Girl, BuyTogether,ChangHua, Chiayi, ChungLi, Daliao,\
			FengYuan, FongShan, Food, FuMouDiscuss, Gossiping, Hate, Hsinchu,Hualien, I_Lan, Jinmen,\
			Kaohsiung, Keelung, Linyuan, LoL, Matsu, MenTalk, Miaoli, NBA, Nantou, PH_sea, PingTung,\
			PuzzleDragon, Sad,Stock, StupidClown, TaichungBun, TaichungCont, Tainan, Taitung, Taoyuan,\
			ToS, WomenTalk, Yunlin, ask, happy, home_sale, iPhone, joke, movie, prozac]

test_data = []
count_num = []
punctuations = '[A-Za-z0-9]|\n|\?|\？|\.|。|，|\^|\s|=|:|：|；|、|！|\!|\/|\／|\）|\(|\）|（|「|」|>|<|"|~|\「|\」|\:|◎|\☆|\Σ|\-|~|˙|→|一|_+|'

# count post number within a single board

for boards in ptt_boards:
	count = 0
	for posts in boards.find({},{'content_seg':True})[:]: #adjust numbers of data here
		count_num.append([posts['content_seg']]) #for posts index

		count +=1
	count = count/4
	print('Processing board name: ',boards,'with ',int(count),'posts')
	for posts in boards.find({},{'content_seg':True})[:int(count)]: 
		
		try:
			articles = [i[0] for i in list(posts.values())[0]]
		except:
			articles = [i[0] for i in list(posts.values())[1]]

		articles = [re.sub(punctuations,'', i) for i in articles]
		test_data.append(articles)

test_data = [[subelt for subelt in elt if subelt != '' ] for elt in test_data]
# print(test_data)


# # # # --- train word embedding --- #
print('Training Word2Vec model...')

model = gensim.models.word2vec.Word2Vec(sentences= test_data, size=100, alpha=0.025, window=10, min_count=5,\
		 max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5,\
		 cbow_mean=1, iter=5, null_word=0, trim_rule=None, sorted_vocab=1,\
		 batch_words=10000)

# # # # # --- write training result as python pickle file --- #
print('Writing taining result as pickle...')
filename = 'word_embedding_model_2.sav'
pickle.dump(model, open(filename, 'wb'))
print('Finished')

# # # --- load the model from pickle --- #
# loaded_model = pickle.load(open(filename, 'rb'))


# # # --- view trained result --- #
# res = loaded_model.wv.most_similar(positive = ['台大'], topn = 100) # find the top relevant words to target word
# res = loaded_model.wv.most_similar(positive = ['自己'], topn = 100) # find the top relevant words to target word
# print(res)

# ### ---- threshold testing ---- ###  # let the num be 0.9360
# w2v_res = []
# for aa in res:
# 	if aa[1] > 0.9360:
# 		w2v_res.append(aa[0])
# print(len(w2v_res))











































