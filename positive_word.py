#参考： http://qiita.com/naoyu822/items/473756fb8e8bbdc4d734
#       http://qiita.com/toshikiohnogi/items/9dcdea40a63a293656e8
#		https://libraries.io/pypi/mecab-python-windows
#		pip install mecab-python-windows==0.9.9.6
#		単語の数え上げ
#		https://gist.github.com/hachibeeDI/6716011


#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
fp = FontProperties(fname=r'C:\Users\kt\Desktop\neko\ipagp.ttf', size=14)

import sys
param = sys.argv
infile = "neko.txt.mecab.0" #param[1]

f = open(infile, 'r', encoding='utf-8')
line = f.readline() 
all_words =[]
import MeCab
m = MeCab.Tagger()

from collections import defaultdict
frequency = defaultdict(int)

while line:
    res = m.parseToNode(line)

    while res:
        # print (res.feature)
        # 名詞,一般,*,*,*,*,犬,イヌ,イヌ
        arr = res.feature.split(",")
        class_1 = arr[0]
        frequency[class_1] += 1
        if class_1 == '感動詞':
            all_words.append(arr[6])
            #print (arr[6])
        res = res.next

    line = f.readline()

#print (words)
word_and_counts = {}
top_w = []
top_c = []

for word in all_words:
    if word_and_counts.get(word):
        word_and_counts[word] += 1
    else:
        word_and_counts[word] = 1

for w, c in sorted(word_and_counts.items(), key=lambda x: x[1], reverse=True):
 print (w, c)
 
h = sorted(word_and_counts.items(), key=lambda x: x[1], reverse=True);

print (len(word_and_counts))

top = len(word_and_counts)

for i in range(top):
    top_w.append(h[i][0])
    top_c.append((float)(h[i][1]))

comp = [i for i in range(top)]

plt.xticks(comp,top_w,rotation=90,fontproperties=fp,fontsize ="small")
plt.ylabel(r"回数", fontsize="small", fontproperties=fp) # y軸

left = np.array(comp)
height = np.array(top_c)
plt.bar(left, height, align="center")

plt.show()
