import gensim
import logging

## ---- CORPUS TRAINING ---- ##
# --- assign training data --- #
sentence = [['我','拿'],['我','看']]  # 在list裡面放清乾淨、段好詞的句子 [content]
model = gensim.models.Word2Vec(sentence, min_count=1)  # min_count 低頻詞 / worker 工作環境 / window 上下文 / size vector的數量

# --- trained result --- #
model.wv['拿']  # 100 array

# model.wv.most_similar(positive = ['你','拿']) # "拿"的相似字
model.wv.most_similar(positive = ['我','拿']) 

print(model.wv.similarity('拿', '看')) # 兩的字的distance






