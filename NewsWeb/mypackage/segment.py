import pandas as pd
import jieba


#取停用词词表
stopwords_path = r"/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/stopwords.txt"  # 停用词合集
stop_list = [line.strip() for line in open(stopwords_path, encoding='UTF-8').readlines()]

#函数构造
def participles(string):
    words = jieba.cut(string)
    text = ""
    for word in words:
        if word not in stop_list:
            text += word + ' '
    return text
def seg_depart(data):
    for indexs in data.index:
        data.at[indexs,'txt'] = participles(data.at[indexs,'txt'])
        #print(data.at[indexs,'txt'])
        data.at[indexs,'title'] = participles(data.at[indexs,'title'])
        #print(data.at[indexs,'title'])
    return data

