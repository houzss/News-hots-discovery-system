# coding=utf-8
import numpy as np
import random
from collections import defaultdict
from decimal import Decimal

input_path = 'Data/2.txt'       # 分词，去停用词之后的词集合
###此方法为迭代式方法，暂不考虑

def write(alist, out_path):
    f = open(out_path, 'w', encoding="UTF-8-sig")
    for line in alist:
        f.write(str(line)+'\n')
        # print(line)
    f.close()


def get_doc(path):
    '''
    数据库中得到原有的标签和根据聚类结果得到现有的标签
    '''
    return data_origin, data_now


def get_vector(data1, data2):
    key_word = []
    for word in data1:
        if word not in key_word:
            key_word.append(word)
        else:
            pass
    for word in data2:
        if word not in key_word:
            key_word.append(word)
        else:
            pass
        # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(data1)):
            if key_word[i] == data1[j]:
                word_vector1[i] += 1
        for k in range(len(data2)):
            if key_word[i] == data2[k]:
                word_vector2[i] += 1
    # print(word_vector1)
    # print(word_vector2)
    return word_vector1, word_vector2

def get_cos(vec1, vec2):
    dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    # dist1 = Decimal(dist1).quantize(Decimal('0.000'))
    return dist1

def get_all_cos(data):
    # all_cos[len(data)][len(data)]
    lenth = len(data)
    # lenth = 10
    matrix = [[0 for i in range(lenth)] for i in range(lenth)]
    for i in range(lenth):
        data1 = data[i]
        for j in range(i, lenth):
            data2 = data[j]
            vec1, vec2 = get_vector(data1, data2)
            cos = get_cos(vec1, vec2)
            matrix[i][j] = cos
    for i in range(lenth):
        print(matrix[i])

def main():

    data_origin, data_now = get_doc(input_path)
    '''确定阈值的值'''
    threshold = 0.8
    for i in data_now:
        sim = []
        for j in data_origin:
            vec1, vec2 = get_vector(i, j)
            similarity = get_cos(vec1, vec2)
            sim.append(similarity)
        max = max(sim)
        if max >= threshold:
            position = sim.index(max)
            '''将i加入到position的数据库中'''
        else:
            '''将i重新生成表格加入到数据库中'''

if __name__ == '__main__':
    main()