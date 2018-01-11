import pymongo
from pymongo import MongoClient
import urllib, re, json
import jieba
import gensim
import logging
import pickle
from itertools import chain

# ----- login db ----- #
password = urllib.parse.quote_plus('gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
client = MongoClient('mongodb://achiii:' + password + '@140.112.147.132')

# ----- connect to PTT corpus ----- #
db = client['PTT']

# ----- extract all board names ----- #
board_list = db.collection_names() 
print(board_list)

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

# ----- set ref corpus ----- #
test_data = []
ptt_posts = []

ptt_boards = [AllTogether, Baseball, Beauty, Boy_Girl, BuyTogether,ChangHua, Chiayi, ChungLi, Daliao,\
			FengYuan, FongShan, Food, FuMouDiscuss, Gossiping, Hate, Hsinchu,Hualien, I_Lan, Jinmen,\
			Kaohsiung, Keelung, Linyuan, LoL, Matsu, MenTalk, Miaoli, NBA, Nantou, PH_sea, PingTung,\
			PuzzleDragon, Sad,Stock, StupidClown, TaichungBun, TaichungCont, Tainan, Taitung, Taoyuan,\
			ToS, WomenTalk, Yunlin, ask, happy, home_sale, iPhone, joke, movie, prozac]

for boards in ptt_boards:
	print('Processing content in ptt board:', boards.name)
	for posts in boards.find({},{'content':True})[:1000]: # change the number of post here!
		test_data.append([posts['content']])
# print(test_data) # test_data contains all the posts in ptt_boards


# ----- data cleaning and re-segmentation with user-defined dict  ----- #
punctuations = '\n|\?|\？|\.|。|，|\^|\s|=|、|！|\!|\/|\／|\）|\(|\）|>|<|"||\「|\」|\:|◎|\☆|\Σ|\-|~|˙|→|一|_+|'

for content in test_data:
	print(test_data.index(content)+1,'/',len(test_data))
	for post in content:
	# for nums in [position for position, article in enumerate(content)]:
		stopword = open('stopword.txt','r', encoding='utf8').read()
		jieba.load_userdict('aged.lexicon/target.test.txt') # seg by test word list
		clean_content = re.sub(punctuations,'', post)
		word = jieba.cut(clean_content, cut_all=False)
		ptt_posts.append([i for i in word if i not in stopword])

# print(ptt_posts) # ptt_posts contains all the segmented sentences in all the ptt_boards

# ----- train word embedding ----- #
print('Training Word2Vec model...')
# model = gensim.models.Word2Vec(ptt_posts, min_count=1)  
model = gensim.models.word2vec.Word2Vec(sentences= ptt_posts, size=100, alpha=0.025, window=10, min_count=5,\
		 max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5,\
		 cbow_mean=1, iter=5, null_word=0, trim_rule=None, sorted_vocab=1,\
		 batch_words=10000) # train ptt sentences with w2v model

# ----- write training result as python pickle file ----- #
print('Writing taining result as pickle...')
filename = 'word_embedding_model.sav'
pickle.dump(model, open(filename, 'wb'))
print('Finished')

# ----- load model from pickle ----- #
loaded_model = pickle.load(open(filename, 'rb'))

# ----- view trained result ----- #
'''
測試：以10個relevant words為一組單位，每一個age category隨機選兩個詞彙，人工檢查該target word (e.g 正妹) 所產出的 relevant words中，
語意不合理的範圍在哪裡，並將不合理的semantic distance值設為threshold，抓出threshold以上的relevant word數量
'''
res = loaded_model.wv.most_similar(positive = ['淑女'], topn = 10000) 
# find the top 10000 relevant words and values to target word

# ----- threshold testing ----- #  # let the num be 0.537275

'''
Threshold 的決定方法：將三個category中怪異詞range的最大值和最小值加總平均
最大值：0.60749
最小值：0.46706
最終threshold: 0.537275
'''
w2v_res = []
for relevant_word in res:
	if relevant_word[1] > 0.537275:
		w2v_res.append(relevant_word[0])
print(len(w2v_res)) # number of relevant words above threshold value


'''
[ptt 總版數]  49個

[ptt 所有版的po文數量(放進w2v訓練的data數量)]  3,888,530

[用來做測試的target word與抓到怪異詞的value (以10個詞為一個range)]
Category: l
word: 淑女
怪異詞range: 變速(0.54412) - 法拉力 (0.53880)
word: 紳士
怪異詞range: 傻大姐(0.48208) - 裝扮 (0.47884)

Category: m
word: 人妻
怪異詞range: 謝承均(0.57328) - 未亡人 (0.56730)
word: 帥哥
怪異詞range: 真正(0.60749) - 正到 (0.60422)

Category: s
word: 肥宅
怪異詞range: 人一(0.46820) - 漂亮女孩 (0.46706)
word: 正妹
怪異詞range: 錢帥(0.49944) - 正到 (0.49867)

[Threshold&在評估值裡面的詞彙數量]
Threshold = 0.537275
Category: l (11 words)
淑女	53
紳士	19
嬌娃	809
姑娘	71
夥計 1	
女士	16
君子	154
大哥	31
大姊	not in vocabulary
少年	27
小子	7

Category: m (11 words)
美女	270
帥哥	435
優質	7
人氣	70
人妻	157
色狼	147
女友	124
男友	132
老公	371
老婆	351
太太	124

Category: s (11 words)
潮男	not in vocabulary
網美	378
型男	not in vocabulary
熟女	160
大媽	36
女神	263
正妹	332
美眉	263
肥宅	215
宅男	not in vocabulary
辣妹	223
'''







































