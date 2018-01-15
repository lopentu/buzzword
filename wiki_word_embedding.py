# -*- coding: utf-8 -*- 
import jieba
import gensim
import pickle
import re

# ----- read converted traditional_zh_wiki data ----- #
wiki = open('traditional_zh_wiki_utf-8','r').readlines()

# ----- data cleaning and re-segmentation with user-defined dict  ----- #
wiki_posts = []
for content in wiki[:]: 
	stopword = open('stopword.txt','r', encoding='utf8').read()
	jieba.load_userdict('target.test.txt') # seg by test word list
	clean_content = re.sub(' ','', content)
	word = jieba.cut(clean_content, cut_all=False)
	wiki_posts.append([i for i in word if i not in stopword])
	print('Processing ',wiki.index(content)+1,'/',len(wiki))
print('='*40)

# print(wiki_posts)
print('total number of sentences',len(wiki_posts))  # total:306,129 wiki posts

# ----- train word embedding ----- #
print('='*40)
print('Start training Word2Vec model...')
model = gensim.models.word2vec.Word2Vec(sentences= wiki_posts, size=100, alpha=0.025, window=10, min_count=5,\
		 max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5,\
		 cbow_mean=1, iter=5, null_word=0, trim_rule=None, sorted_vocab=1,\
		 batch_words=10000) # train wiki sentences with w2v model

# ----- write training result as python pickle file ----- #
print('='*40)
print('Writing taining result as pickle...')

filename = 'wiki_word_embedding_model.sav'
pickle.dump(model, open(filename, 'wb'))
print('W2V Training Finished!')
print('='*40)

## ----- 詞彙測試 ---- #

## ----- load model from pickle ----- #
loaded_model = pickle.load(open(filename, 'rb'))

res = loaded_model.wv.most_similar(positive = ['淑女'], topn = 1000)

num = 1
for i in res:
	print(num,i)
	num +=1


'''
[資料來源] wikipedia   

[文章數量(放進w2v訓練的data數量)] 306,129 posts

[用來做測試的target word與抓到怪異詞的value (以10個詞為一個range)]
Category: l
word: 淑女
怪異詞range: 女飾(0.59587) - 笨丈夫(0.59243)
word: 紳士
怪異詞range: 御廚(0.40847) - 加拿大勳(0.40768)

Category: m
word: 人妻
怪異詞range: 沈玉琳(0.46814) - 仕事(0.46727)
word: 帥哥
怪異詞range: 愛搞(0.62271) - 女性格(0.62149)

Category: s
word: 肥宅
怪異詞range: 非常帥(0.46381) - cpv(0.46193)
word: 正妹
怪異詞range: 包小柏(0.61574) - 翁立友(0.61501)


Threshold 的決定方法：將三個category中怪異詞range的最大值和最小值加總平均
最大值：0.62271
最小值：0.40768
最終threshold: 0.515195
'''
res = loaded_model.wv.most_similar(positive = ['辣妹'], topn = 10000)

w2v_res = []
for relevant_word in res:
	if relevant_word[1] > 0.515195:
		w2v_res.append(relevant_word[0])
print(len(w2v_res)) # number of relevant words above threshold value

'''
[Threshold&在評估值裡面的詞彙數量]
Threshold = 0.515195
Category: l (11 words)
淑女	690
紳士	6
嬌娃	6597
姑娘	37
夥計 3499
女士	15
君子	1034
大哥	267
大姊	1539
少年	46
小子	106

Category: m (11 words)
美女	325
帥哥	1784
優質	55
人氣	16 
人妻	65
色狼	2685
女友	1831
男友	1989
老公	2880
老婆	841
太太	1449

Category: s (11 words)
潮男	3542
網美	159
型男	2166
熟女	210
大媽	2720
女神	53
正妹	4063
美眉	1218
肥宅	2
宅男	821
辣妹	1993

'''



