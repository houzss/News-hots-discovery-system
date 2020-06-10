# coding=utf-8
import random
from math import sqrt
import math
import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans
from Bio.Cluster import kcluster
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics
import pandas as pd
import json
import time
from segment import *
from db_operate import *
import re
import sys

def listToJson(lst):
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json

def get_name_batch(text):
    return re.findall( r'(\w{2})_(\d{14})', text).pop()

def get_doc1(data):  # get_doc1
    datas = np.array(data, dtype=float)
    return datas



def get_alldoc(data):  # get_alldoc
    df = data['txt']
    data_list = []
    for i in range(len(df)):
        m = df[i].strip().split()
        # print(m)
        data_list.append(m)
    return data_list


def get_doc(data):  # get_doc
    # 得到词袋
    all_list = []
    for text in data:
        all_list += text
    corpus = set(all_list)  # 去重
    corpus_dict = dict(zip(corpus, range(len(corpus))))
    return corpus_dict


def get_vector(data, corpus_dict):  # 词频计算
    # 总词频统计
    doc_frequency = defaultdict(int)
    for word_list in data:
        doc_frequency[word_list] += 1
    # 计算每个词的TF值
    word_tf = {}  # 存储每个词的tf值
    for i in doc_frequency:
        word_tf[i] = doc_frequency[i] / sum(doc_frequency.values())
    # 计算每个词的IDF值
    doc_num = len(data)
    word_idf = {}  # 存储每个词的idf值
    word_doc = defaultdict(int)  # 存储包含该词的文档数
    for i in doc_frequency:
        for j in data:
            if i in j:
                word_doc[i] += 1
    for i in doc_frequency:
        word_idf[i] = math.log(doc_num / (word_doc[i] + 1))
    # 计算每个词的TF*IDF的值
    word_tf_idf = {}
    for i in doc_frequency:
        word_tf_idf[i] = word_tf[i] * word_idf[i]
    word_vector = np.zeros(len(corpus_dict))
    for word in data:
        i = corpus_dict[word]
        word_vector[i] = word_tf_idf[word]
    # write(word_vector, out_path)
    return word_vector


def orderdic(dic, reverse):
    ordered_list = sorted(dic.items(), key=lambda item: item[1], reverse=reverse)
    return ordered_list


def get_Kmeans(data, n, category):
    clusterid, error, nfound = kcluster(data, n, dist='u', npass=10)
    cluster = []
    for i in range(n):
        cluster.append([])
    for i in range(len(category)):
        cluster[clusterid[i]].append(category[i])
    score = metrics.silhouette_score(data, clusterid, metric='cosine')  # 轮廓系数
    # score = metrics.silhouette_score(data, clusterid)  # 轮廓系数
    #print(score)
    return cluster, score


def get_Agg(data, n, category):
    agg = AgglomerativeClustering(n_clusters=n, affinity='cosine', linkage='average')
    label = agg.fit_predict(data)
    cluster = []
    for i in range(n):
        cluster.append([])
    for i in range(len(category)):
        cluster[label[i]].append(category[i])
    return cluster


def get_cos(vec1, vec2):
    dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return dist1


def position(vec_list):  # UPGMA
    x = 0
    y = 0
    min_dis = -1000
    similarityv = -1000
    for i in range(0, len(vec_list)):
        for j in range(i + 1, len(vec_list)):
            similarityv = get_cos(vec_list[i], vec_list[j])
            if similarityv > min_dis:
                min_dis = similarityv
                x = i
                y = j
    return x, y


def listadd(listx, listy):
    return [(listx[i] + listy[i]) / 2 for i in range(0, len(listx))]


def get_AgglomerateTree(data, n):  # 得到凝聚树
    vec_list = []
    log = []
    for i in range(len(data)):
        vec_list.append(data[i])
    while len(vec_list) > n:
        x, y = position(vec_list)
        log.append((x, y))
        addlist = listadd(vec_list[x], vec_list[y])
        vec_list.append(addlist)
        del vec_list[x]
        del vec_list[y - 1]
    return log


def get_cluster(data, log_list):  # 通过凝聚树得到簇
    cluster = []
    for i in range(len(data)):
        s = [i]
        cluster.append(s)
    for lo in log_list:
        # tem=[]
        # tem.append(sent[lo[0]])
        # tem.append(sent[lo[1]])
        tem = cluster[lo[0]] + cluster[lo[1]]
        if lo[0] < lo[1]:
            del cluster[lo[0]]
            del cluster[lo[1] - 1]
        else:
            del cluster[lo[1]]
            del cluster[lo[0] - 1]
        cluster.append(tem)
    return cluster


def get_score(vector, cul):
    label = np.zeros(len(vector))
    for i in range(len(cul)):
        for j in cul[i]:
            label[j] = int(i)

    score = metrics.silhouette_score(X=vector, labels=label, metric='cosine')
    return score


def clustering(csv_filename):
    timesp = time.localtime()
    timestamp = time.strftime("%Y%m%d%H%M%S", timesp)
    web,batch = get_name_batch(csv_filename)
    filepath = r'/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/csv/' + str(csv_filename) + '.csv'
    vector_path = r'/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/vectors/' + str(csv_filename) +'.json'
    datas = pd.read_csv(filepath, sep='\t')

    data = seg_depart(datas)

    # start = time.process_time()#用于计算运行时间

    # 得到所有的分词好的文本和词袋
    all_doc = get_alldoc(data)
    all_corpusdict = get_doc(all_doc)
    # 得到全部文本集的向量
    all_vector = []
    for i in range(len(all_doc)):
        vec = get_vector(all_doc[i], all_corpusdict)
        all_vector.append(vec)
    all_vector = np.array(all_vector)
    #print(all_vector)
    # K-means聚类
    cul = []
    for i in range(len(all_vector)):
        cul.append(i)
    len1 = len(all_vector)
    if len1 < 150:
        n = round(math.sqrt(len1))
    else:
        n = round(len1 / 20)
    if n <= 1:
        n = 2
    #print('n:' + str(n))
    K_cul, score_K = get_Kmeans(all_vector, n, cul)#随机函数，结果不一致
    #print(K_cul)
    #print(score_K)
    # 对每一个K均值得到的簇进行层次凝聚聚类，若簇的大小*0.1<1,则不进行层次凝聚聚类
    Agg = []
    for i in K_cul:
        m = int(len(i) * 0.1)
        if m <= 1:
            Agg.append(i)
        else:
            # print(all_vector[i])
            cul = get_Agg(all_vector[i], m, i)
            Agg += cul
    #print(Agg)

    score_Agg = get_score(all_vector, Agg)
    #print(score_Agg)

    # n = int(len(all_doc)/20)

    # 计算每个簇的质心
    centroid = []
    for i in Agg:
        b = np.sum(all_vector[i], axis=0) / len(i)
        centroid.append(b)

    cul = []
    for j in range(len(Agg)):
        cul.append(j)
    # 根据簇心对每个簇进行层次凝聚
    Log = get_Agg(centroid, n, cul)
    # print(Log)
    Final_cul = []
    for j in Log:
        cul = []
        for p in j:
            cul = cul + Agg[p]
        Final_cul.append(cul)
    #print(Final_cul)
    # print(len(Final_cul))

    score_end = get_score(all_vector, Final_cul)
    #print(score_end)

    # 寻找轮廓系数最大的方案
    if score_K >= score_Agg:
        score_max = score_K
    else:
        score_max = score_Agg
        if score_max >= score_end:
            score_max = score_max
        else:
            score_max = score_end
    if score_max == score_K:
        Final = K_cul
    elif score_max == score_Agg:
        Final = Agg
    else:
        Final = Final_cul

    #print(score_max)
    #print(Final)
    #print(len(Final))

    # 将轮廓系数最大的方案输出到Clustering_results.csv中
    # f = open('./clustering_result.csv', 'w', encoding="UTF-8-sig")
    clustering_results = {}
    count = 1
    for line in Final:
        #字典构造
        clustering_result = {}
        clustering_result['clusterid'] = timestamp + str(count)
        clustering_result['categoryid'] = count
        clustering_result['clusternum'] = str(len(line))
        clustering_result['web'] = web
        clustering_result['batch'] = batch
        clustering_result['vectors'] = str(line)
        clustering_result['clusterbatch'] = timestamp

        clustering_results[str(count)] = clustering_result
        #print(clustering_result)
        count += 1
    #print(clustering_results)
    write_into_db_cluster(clustering_results,len(Final))
    with open(vector_path,'w') as f:
        f.write(json.dumps(Final))

        # f.write(str(line) + '\n')
        #print(line)
        #print(len(line))
    # f.close()
    result = {'clustered_batch':timestamp}
    result_json = json.dumps(result)
    print(result_json)
    # end = time.process_time()
    # print("final is in ", end - start)
def mains(argv):
    clustering(argv[1])
    #filename= 'nf_20200512220444'
    #clustering(filename)
if __name__ == '__main__':
    mains(sys.argv)

