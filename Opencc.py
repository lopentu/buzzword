from opencc import OpenCC 
openCC = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese
# can also set conversion by calling set_conversion
# openCC.set_conversion('s2tw')

wiki = open('wiki.zh.text','r').readlines()

file = open('traditional_zh_wiki','w')
for i in wiki[:]:
	converted = openCC.convert(i)
	file.write(converted)
file.close()

