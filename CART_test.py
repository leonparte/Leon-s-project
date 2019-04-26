# -*- coding: cp936 -*-

import csv
from numpy import *

filename = '西瓜数据集02.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    print(header_row)

# 将数据集存储到字典之中
    watermalons = []

    for row in reader:
        new_watermalon = {'色泽':row[1],'根蒂':row[2],'敲声':row[3],'纹理':row[4],'脐部':row[5],'触感':row[6],'value':row[7]}
        watermalons.append(new_watermalon)

# 下面来求样本集中好瓜与坏瓜的个数，value_0为坏瓜，value_1为好瓜
    value_0 = 0
    value_1 = 0

    i = 0
    for watermalon in watermalons:
        if watermalon['value'] == '是':
            value_1 += 1
        elif watermalon['value'] == '否':
            value_0 += 1
        else:
            print("EORRO!")
            break
        i += 1
    sum = len(watermalons)
    print("西瓜的总数为：", sum, "\n其中，好瓜的个数为：", value_1, ";坏瓜的个数为:", value_0)

    labels = []
    for index, column_header in enumerate(header_row):
        labels.append(column_header)

# 下面求出了初始信息增益(Ent_ini)
    Ent_ini = - value_1 / sum * math.log(value_1 / sum) / math.log(2) \
              - value_0 / sum * math.log(value_0 / sum) / math.log(2)

    print("初始信息熵为：", Ent_ini, "\n")
    D_ini = {"value": len(watermalons), "Ent": Ent_ini, "p": 1}

# 统计西瓜中某属性m的数量以用于计算信息
    def num_of_m(m):
        i = 0
        num_ms = []
        ini_m = {watermalons[i][m]: 0, 'value': 0}
        num_ms.append(ini_m)
        while i <= len(watermalons) - 1:
            j = 0  # j为“颜色种类数”数组长度
            flag = 1  # 标志，flag为真则说明该轮遍历到了新的颜色，需要增加数组长度
            while j < len(num_ms):
                if num_ms[j].__contains__(watermalons[i][m]):
                    num_ms[j][watermalons[i][m]] += 1
                    if watermalons[i]['value'] == '是':
                        num_ms[j]['value'] += 1
                    flag = 0
                    break
                else:
                    j += 1
            if flag:
                if watermalons[i]['value'] == '是':
                    new_m = {watermalons[i][m]: 1, 'value': 1}
                else:
                    new_m = {watermalons[i][m]: 1, 'value': 0}
                num_ms.append(new_m)

            i += 1
        return num_ms

# 求m属性的好瓜率
    def pe(m):
        i = 0
        while i < len(m):
            p = 0;
            flag = 0;
            for d in m[i]:
                if flag == 0:
                    p = 1 / m[i][d]
                    flag = 1
                else:
                    p *= m[i][d]
            m[i]['p'] = p # 为字典m添加‘p’项
            i += 1

# 求m属性各取值相对应的基尼系数
    def Gini_attr(m):
        i = 0
        e = 0
        Gini = 10000
        while i < len(m):
            p_1 = m[i]['p']
            p_0 = 1 - p_1
            g = 1 - p_1 * p_1 - p_0 * p_0
            m[i]['gini'] = g
            i += 1


    def Gini_i_attr(M,m):
        i = 0
        e = 0
        while i < len(m):
            p_1 = m[i]['p']
            if p_1 == 0:
                i += 1
                continue
            e += (m[i]['value']/m[i]['p'])/(M['value']/M['p']) * m[i]['gini']
            i += 1
        return (e)


# 统计各属性的数量
    nums = [None]
    nums.append(num_of_m('色泽'))
    nums.append(num_of_m('根蒂'))
    nums.append(num_of_m('敲声'))
    nums.append(num_of_m('纹理'))
    nums.append(num_of_m('脐部'))
    nums.append(num_of_m('触感'))

    Gini_i = [1000]  # 初始化信息增益率
    Gini = [1000]
    sum_color = 0  # 初始化本组数据个数

# 计算各属性各具体取值对应的好瓜率，并计算各属性对应的信息增益并增加到信息增益数组Ent中
    i = 1
    while i < 7:
        print(nums[i])
        pe(nums[i])
        print(nums[i])
        Gini_attr(nums[i])
        print(nums[i])
       # print(labels[i], "的基尼值为：", nums[i])
        #Gini.append(Gini_attr(nums[i]))
#        print(labels[i], "的基尼值为：", Gini[i])
        Gini_i.append(Gini_i_attr(D_ini, nums[i]))
        i += 1
    Gini_i.append(None)

    i = 0
    for index, column_header in enumerate(header_row):
        print(index, column_header, Gini_i[i])
        i += 1
        if i == 7:
            print("\n")
            break

    min = 1000 # 初始化“min”
    m = 0 # m用于记录min的位置
    for i in range(1, 6):
        if Gini_i[i] < min:
            m = i
            min = Gini_i[i]
        i = i + 1

    print("选择第", m, "个属性：“", labels[m], "”作为划分属性，其基尼系数为：Gini_i[m] = ", Gini_i[m])