# -*- coding: utf-8 -*- 

import gensim
import pickle

# # PTT model
# filename = '../PttCropus/word_embedding_model.sav'
# loaded_model = pickle.load(open(filename, 'rb'))

# # load top 1000 high frequent word from moe dict 

# with open('top1000_filtered_dict.txt') as f:
#     file = f.read().splitlines() 

# # 

# # moe_ptt_result = []
# for moe_word in file:
# 	# f = open('moe_ptt_result', 'w')
# 	try:
# 		res = loaded_model.wv.most_similar(positive = [moe_word], topn = 10000)
# 		w2v_res = []
# 		for relevant_word in res:
# 			if relevant_word[1] > 0.537275:
# 				# print(moe_word,len(relevant_word[0]))
# 				w2v_res.append(relevant_word[0])
# 		# f.write(moe_word+len(w2v_res)+'\n')
# 		print(moe_word,' ',len(w2v_res))

# 	except:
# 		print(moe_word, 'not in vocabulary')
# 		# f.write(moe_word+' not in vocabulary'+'\n')
# 		# moe_ptt_result.append(moe_word+' not in vocabulary')
# # print(moe_ptt_result)


# Wiki model
filename = '../wikicorpus/wiki_word_embedding_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# load top 1000 high frequent word from moe dict 

with open('top1000_filtered_dict.txt') as f:
    file = f.read().splitlines() 

# 

# moe_ptt_result = []
for moe_word in file:
	# f = open('moe_ptt_result', 'w')
	try:
		res = loaded_model.wv.most_similar(positive = [moe_word], topn = 100000) #Wiki 上限改成100,000，超過100,000以100,000計算
		w2v_res = []
		for relevant_word in res:
			if relevant_word[1] > 0.515195:
				# print(moe_word,len(relevant_word[0]))
				w2v_res.append(relevant_word[0])
		# f.write(moe_word+len(w2v_res)+'\n')
		print(moe_word,' ',len(w2v_res))

	except:
		print(moe_word, 'not in vocabulary')
		# f.write(moe_word+' not in vocabulary'+'\n')
		# moe_ptt_result.append(moe_word+' not in vocabulary')
# print(moe_ptt_result)