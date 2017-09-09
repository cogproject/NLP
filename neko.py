#参考 http://qiita.com/Masaaki_Inaba/items/eb33cf9a3bb79102ff5c#37-%E9%A0%BB%E5%BA%A6%E4%B8%8A%E4%BD%8D10%E8%AA%9E--38-%E3%83%92%E3%82%B9%E3%83%88%E3%82%B0%E3%83%A9%E3%83%A0--39-zipf%E3%81%AE%E6%B3%95%E5%89%87
#MeCab install 参考　http://d.hatena.ne.jp/mahan/20120618/1340040589

import MeCab
import ngram
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#def make_analyzed_file(input_file_name: str, output_file_name: str) -> None:
#    """
#    プレーンな日本語の文章ファイルを形態素解析してファイルに保存する.
#    :param input_file_name プレーンな日本語の文章ファイル名
#    :param output_file_name 形態素解析済みの文章ファイル名
#    """
#    _m = MeCab.Tagger("-Ochasen")
#    with open(input_file_name, encoding='utf-8') as input_file:
#        with open(output_file_name, mode='w', encoding='utf-8') as output_file:
#            output_file.write(_m.parse(input_file.read()))
#
#make_analyzed_file('neko.txt', 'neko.txt.mecab')


def tabbed_str_to_dict(tabbed_str: str) -> dict:
    """
    例えば「次第に   シダイニ    次第に   副詞-一般   」のようなタブ区切りで形態素を表す文字列をDict型に変換する.
    :param tabbed_str タブ区切りで形態素を表す文字列
    :return Dict型で表された形態素
    """
    elements = tabbed_str.split()
    
    if 0 < len(elements) < 4:
        return {'surface': elements[0], 'base': '', 'pos': '', 'pos1': ''}
    else:
        return {'surface': elements[0], 'base': elements[1], 'pos': elements[2], 'pos1': elements[3]}


def morphemes_to_sentence(morphemes: list) -> list:
    """
    Dict型で表された形態素のリストを句点毎にグルーピングし、リスト化する.
    :param morphemes Dict型で表された形態素のリスト
    :return 文章のリスト
    """
    sentences = []
    sentence = []
    
    for morpheme in morphemes:
        sentence.append(morpheme)
        
        if morpheme['pos1'] == '記号-句点':
            sentences.append(sentence)
            sentence = []

    return sentences


with open('neko.txt.mecab.0', encoding='utf-8') as file_wrapper:
    morphemes = [tabbed_str_to_dict(line) for line in file_wrapper]



sentences = morphemes_to_sentence(morphemes)


# 結果の確認
#print(morphemes)
#print(sentences[::100])

verbs_surface = [morpheme['surface'] for morpheme in morphemes if morpheme['pos1'].find('動詞') == 0]
verbs_base = [morpheme['base'] for morpheme in morphemes if morpheme['pos1'].find('動詞') == 0]
nouns_suru = [morpheme['surface'] for morpheme in morphemes if morpheme['pos1'] == '名詞-サ変接続']


# 結果の確認
#print(verbs_surface)
#print(verbs_base)
#print(nouns_suru)


def ngramed_list(lst: list, n: int = 3) -> list:
    """
    listをNグラム化する.
    :param lst Nグラム化対象のリスト
    :param n N (デフォルトは N = 3)
    :return Nグラム化済みのリスト
    """
    index = ngram.NGram(N=n)
    return [term for term in index.ngrams(lst)]


def is_noun_no_noun(words: list) -> bool:
    """
    3つの単語から成るリストが「名詞-の-名詞」という構成になっているかを判定する.
    :param words 3つの単語から成るリスト
    :return bool (True:「名詞-の-名詞」という構成になっている / False:「名詞-の-名詞」という構成になっていない)
    """
    return (type(words) == list) and (len(words) == 3) and \
           (words[0]['pos1'].find('名詞') == 0) and \
           (words[1]['surface'] == 'の') and \
           (words[2]['pos1'].find('名詞') == 0)


# 「名詞-の-名詞」を含むNグラムのみを抽出
noun_no_noun = [ngrams for ngrams in ngramed_list(morphemes) if is_noun_no_noun(ngrams)]

# 表層を取り出して結合する
noun_no_noun = [''.join([word['surface'] for word in ngram]) for ngram in noun_no_noun]

# 結果の確認
print(len(noun_no_noun))
#print(noun_no_noun[0])
#print(noun_no_noun[1])
#print(noun_no_noun[2])


def morphemes_to_noun_array(morphemes: list) -> list:
    """
    辞書型で表された形態素のリストを句点もしくは名詞以外の形態素で区切ってグルーピングし、リスト化する.
    :param morphemes 辞書型で表された形態素のリスト
    :return 名詞の連接のリスト
    """
    nouns_list = []
    nouns = []

    for morpheme in morphemes:
        if morpheme['pos1'].find('名詞') >= 0:
            nouns.append(morpheme)
        elif (morpheme['pos1'] == '記号-句点') | (morpheme['pos1'].find('名詞') < 0):
            nouns_list.append(nouns)
            nouns = []

    return [nouns for nouns in nouns_list if len(nouns) > 1]


noun_array = [''.join([noun['surface'] for noun in nouns]) for nouns in morphemes_to_noun_array(morphemes)]

# 結果の確認
for i in range(0,30):
    print(noun_array[i])


def get_frequency(words: list) -> dict:
    """
    単語のリストを受け取って、単語をキーとして、頻度をバリューとする辞書を返す.
    :param words 単語のリスト
    :return dict 単語をキーとして、頻度をバリューとする辞書
    """
    frequency = {}
    for word in words:
        if frequency.get(word):
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency


frequency = get_frequency([morpheme['surface'] for morpheme in morphemes])

# ソート
frequency = [(k, v) for k, v in sorted(frequency.items(), key=lambda x: x[1], reverse=True)]




fig = plt.figure(figsize=(20, 6))

# 37. 出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
words = [f[0] for f in frequency[0:10]]
x_pos = np.arange(len(words))
fp = FontProperties(fname=r'C:\Users\kt\Desktop\neko\ipagp.ttf', size=14)

ax1 = fig.add_subplot(131)
ax1.bar(x_pos, [f[1] for f in frequency[0:10]], align='center', alpha=0.4)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(words, fontproperties=fp)
ax1.set_ylabel('Frequency')
ax1.set_title('Top 10 frequent words')

# 38. 単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．
freq = list(dict(frequency).values())
freq.sort(reverse=True)

ax2 = fig.add_subplot(132)
ax2.hist(freq, bins=50, range=(0, 50))
ax2.set_title('Histogram of word count')
ax2.set_xlabel('Word count')
ax2.set_ylabel('Frequency')

# 39. 単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
rank = list(range(1, len(freq) + 1))

ax3 = fig.add_subplot(133)
ax3.plot(freq, rank)
ax3.set_xlabel('Rank')
ax3.set_ylabel('Frequency')
ax3.set_title('Zipf low')
ax3.set_xscale('log')
ax3.set_yscale('log')

fig.savefig('morphological_analysis.png')

plt.show()





