#coding:utf8
import jieba
import math
import re

pseeds = ("好", "快", "美味", "棒", "美味", "好吃", "赞", "不错",
                  "香", "好评", "喜欢", "给力", "划算", "可口", "很快")

nseeds = ("垃圾", "差评", "慢", "差", "难吃", "生气", "凉", "不给力",
                  "无语", "不值", "不划算", "超时", "不好", )

word_dic = {}
common_word_dic = {}

def create_comments():
    with open("./docs/外卖评论.csv", "r", encoding="utf-8") as file:
        comments = []
        for line in file.readlines():
            comment = jieba.lcut(re.sub('[^\u4e00-\u9fa5]+', '', line)) #正则表达式去除非汉字
            comments.append(comment)
    return comments


def create_dic(comments):
    for comment in comments:
        for word in comment:
            word_dic[word] = word_dic.get(word, 0) + 1              #word_dic 存储单词出现的句子数
            if word in pseeds or word in nseeds:                    #common_word_dic 存储关键词和单词共同出现的句子数
                for tword in comment:
                    if not(tword in pseeds or tword in nseeds):
                        common_word_dic[(word, tword)] = word_dic.get((word, tword), 0) + 1


def create_tendency(comments):
    tendency = {}
    for comment in comments:
        for word in comment:
            if not (word in pseeds or word in nseeds):
                tendency[word] = sopmi(word)
    return tendency

def sopmi(word):
    res = 0
    for pword in pseeds:
        res += pmi(pword, word)

    for nword in nseeds:
        res -= pmi(nword, word)

    return res

def pmi(sword, word):
    return math.log(common_word_dic.get((sword, word), 1e-10) / (word_dic[sword] * word_dic[word]), 2)

def sort_data(tendency):
#返回排好从大到小序的统计数据
    items = list(tendency.items())
    items.sort(reverse=True, key=lambda x: x[1])
    return items

def print_result(items, size=50):
    print("====Top 50 positive words====")
    for i in range(0 , size):
        print("{}\t{}".format(items[i][0], items[i][1]))
    print("\n====Top 50 negative words====")
    for i in range(-1, -1 * size - 1, -1):
        print("{}\t{}".format(items[i][0], items[i][1]))

if __name__ == '__main__':
    comments = create_comments()
    create_dic(comments)
    tendency = create_tendency(comments)
    items = sort_data(tendency)
    print_result(items)