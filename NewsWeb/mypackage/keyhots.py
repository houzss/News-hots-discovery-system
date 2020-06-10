import csv
import datetime
import heapq
import pandas as pd
from jieba import analyse
from textrank4zh import TextRank4Keyword
import sys
import json
import re
import time
from db_operate import *

stopwords_path = r"/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/stopwords.txt"
tr4w = TextRank4Keyword(stop_words_file = stopwords_path)


def get_name_batch(text):
    return re.findall( r'(\w{2})_(\d{14})', text).pop()

def textrank_extract(text, keyword_num):
    textrank = analyse.textrank
    analyse.set_stop_words(stopwords_path)
    keywords = textrank(text, keyword_num)
    # 输出抽取出的关键词
    word1 = ""
    count = 1
    for keyword in keywords:
        if( count == len(keywords)):
            word1 = word1 + keyword
        else:
            word1 = word1 + (keyword + "/ ")
        count += 1
    return word1


def get_keywords(text, keyword_num):
    key = {}
    for i in range(len(text)):
        tr = textrank_extract(text[i], keyword_num)

        key[i] = tr
    return key


# 某一个簇的热度之计算，Cno为簇编号
def calculate(Cno, num, atime):
    S = 0
    N = num  # 所有文章的数量
    #print(num)
    hot = []

    b = 0

    for a in range(len(Cno)):  # 寻找簇内最长时间和最短时间
        n = 0
        MAX = atime[Cno[b][0]]
        MIN = atime[Cno[b][0]]
        for d in range((len(Cno[b]))):
            if MAX < atime[Cno[b][d]]:
                MAX = atime[Cno[b][d]]
                # print(MAX)
            if MIN > atime[Cno[b][d]]:
                MIN = atime[Cno[b][d]]
                # print(MIN)
            n = n + 1

        b = b + 1
        dec = ((MAX - MIN).days)

        Hot = ((n)/(dec+1)) * (n / N)

        no = []
        no.append(a)
        no.append(Hot)
        hot.append(no)

    return hot, b


def getrank(atime, num, cno):
    hot = []
    (hot, b) = calculate(cno, num, atime)

    re2 = heapq.nlargest(10, hot, lambda x: x[1])  # 根据第1+1个的参数截取前10行的参数
    re3 = sorted(re2,key= lambda x:x[0])
    hots_list = [round(i[1],4) for i in re3]
    # print(re2)

    return hots_list


def getmsg(filepath, cno):
    alltxt = []
    data = pd.read_csv(filepath, sep='\t', encoding="utf-8")  # 读取文件

    for i in range(len(cno)):
        txt = ''
        for j in cno[i]:
            txt += data.at[j, 'txt'] + '\n'

        alltxt.append(txt)
    atime = []
    c = []
    for k in data.index:
        row = data.at[k, 'datetime']
        row = row.replace("年", "-").replace("月", "-").replace("日", "").replace(" ", "")
        date1 = datetime.datetime.strptime(row, '%Y-%m-%d%H:%M').date()
        atime.append(date1)

    return alltxt, atime, len(data)
def keyhots(filename,keyword_num,timestamp):
    web, batch = get_name_batch(filename)
    filepath = r'/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/csv/' + str(filename) + '.csv'
    vector_path = r'/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/vectors/' + str(filename) + '.json'
    cno = json.loads([line.strip() for line in open(vector_path, encoding='UTF-8').readlines()].pop())
    #print(json.dumps({'filepath': filepath, 'cno': cno, 'keyword_num': keyword_num}))
    alltxt, atime, num = getmsg(filepath, cno)
    keyhots_dicts ={}
    count = 0

    key_words = get_keywords(alltxt, keyword_num)
    #print(key_words)  # output:关键字
    hots = getrank(atime, num, cno)  # 热度值排序的列表
    #print(hots)
    while count < len(cno):
        keyhots_dict ={}
        keyhots_dict['keyhotsid'] = timestamp + str(count +1)
        keyhots_dict['categoryid'] = count+1
        keyhots_dict['batch'] = batch
        keyhots_dict['keywords'] = key_words[count]
        keyhots_dict['keywords_num'] = keyword_num
        keyhots_dict['hotvalues'] = hots[count]
        keyhots_dict['keyhotsbatch'] = timestamp
        keyhots_dict['web'] =web
        #print(keyhots_dict)
        keyhots_dicts[count] = keyhots_dict
        count += 1
    return keyhots_dicts
def mains(argv):

    #filename = 'bj_20200512200907'
    #keyword_num = 10
    filename = argv[1]
    keyword_num = int(argv[2])
    timesp = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", timesp)
    keyhots_dict = keyhots(filename,keyword_num,timestamp)
    #print(keyhots_dict)
    write_into_db_keyhots(keyhots_dict,len(keyhots_dict))
    result = {'keyhots_batch': timestamp}
    result_json = json.dumps(result)
    print(result_json)
if __name__ == '__main__':
    mains(sys.argv)

