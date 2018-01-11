import gensim
import pickle

filename = 'word_embedding_model.sav'

# ----- load model from pickle ----- #
loaded_model = pickle.load(open(filename, 'rb'))

# ----- view trained result ----- #

'''
測試：以10個relevant words為一組單位，每一個age category隨機選兩個詞彙，人工檢查該target word (e.g 正妹) 所產出的 relevant words中，
語意不合理的範圍在哪裡，並將不合理的semantic distance值設為threshold，抓出threshold以上的relevant word數量
'''
res = loaded_model.wv.most_similar(positive = ['淑女'], topn = 10000) # find the top 1000 relevant words and values to target word

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
		w2v_res.append(res[0])
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

[Threshold與在評估值裡面的詞彙數量]
Threshold = 0.537275
Category: l (11 words)
淑女	l
紳士	l
嬌娃	l
姑娘	l
夥計	l
女士	l
君子	l
大哥	l
大姊	l
少年	l
小子	l

Category: m (11 words)
美女	m
帥哥	m
優質	m
人氣	m
人妻	m
色狼	m
女友	m
男友	m
老公	m
老婆	m
太太	m

Category: s (words)
潮男	s
網美	s
型男	s
熟女	s
大媽	s
女神	s
正妹	s
美眉	s
肥宅	s
宅男	s
辣妹	s
'''
