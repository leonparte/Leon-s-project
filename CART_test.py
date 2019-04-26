# -*- coding: cp936 -*-

import csv
from numpy import *

filename = '�������ݼ�02.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    print(header_row)

# �����ݼ��洢���ֵ�֮��
    watermalons = []

    for row in reader:
        new_watermalon = {'ɫ��':row[1],'����':row[2],'����':row[3],'����':row[4],'�겿':row[5],'����':row[6],'value':row[7]}
        watermalons.append(new_watermalon)

# ���������������кù��뻵�ϵĸ�����value_0Ϊ���ϣ�value_1Ϊ�ù�
    value_0 = 0
    value_1 = 0

    i = 0
    for watermalon in watermalons:
        if watermalon['value'] == '��':
            value_1 += 1
        elif watermalon['value'] == '��':
            value_0 += 1
        else:
            print("EORRO!")
            break
        i += 1
    sum = len(watermalons)
    print("���ϵ�����Ϊ��", sum, "\n���У��ùϵĸ���Ϊ��", value_1, ";���ϵĸ���Ϊ:", value_0)

    labels = []
    for index, column_header in enumerate(header_row):
        labels.append(column_header)

# ��������˳�ʼ��Ϣ����(Ent_ini)
    Ent_ini = - value_1 / sum * math.log(value_1 / sum) / math.log(2) \
              - value_0 / sum * math.log(value_0 / sum) / math.log(2)

    print("��ʼ��Ϣ��Ϊ��", Ent_ini, "\n")
    D_ini = {"value": len(watermalons), "Ent": Ent_ini, "p": 1}

# ͳ��������ĳ����m�����������ڼ�����Ϣ
    def num_of_m(m):
        i = 0
        num_ms = []
        ini_m = {watermalons[i][m]: 0, 'value': 0}
        num_ms.append(ini_m)
        while i <= len(watermalons) - 1:
            j = 0  # jΪ����ɫ�����������鳤��
            flag = 1  # ��־��flagΪ����˵�����ֱ��������µ���ɫ����Ҫ�������鳤��
            while j < len(num_ms):
                if num_ms[j].__contains__(watermalons[i][m]):
                    num_ms[j][watermalons[i][m]] += 1
                    if watermalons[i]['value'] == '��':
                        num_ms[j]['value'] += 1
                    flag = 0
                    break
                else:
                    j += 1
            if flag:
                if watermalons[i]['value'] == '��':
                    new_m = {watermalons[i][m]: 1, 'value': 1}
                else:
                    new_m = {watermalons[i][m]: 1, 'value': 0}
                num_ms.append(new_m)

            i += 1
        return num_ms

# ��m���Եĺù���
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
            m[i]['p'] = p # Ϊ�ֵ�m��ӡ�p����
            i += 1

# ��m���Ը�ȡֵ���Ӧ�Ļ���ϵ��
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


# ͳ�Ƹ����Ե�����
    nums = [None]
    nums.append(num_of_m('ɫ��'))
    nums.append(num_of_m('����'))
    nums.append(num_of_m('����'))
    nums.append(num_of_m('����'))
    nums.append(num_of_m('�겿'))
    nums.append(num_of_m('����'))

    Gini_i = [1000]  # ��ʼ����Ϣ������
    Gini = [1000]
    sum_color = 0  # ��ʼ���������ݸ���

# ��������Ը�����ȡֵ��Ӧ�ĺù��ʣ�����������Զ�Ӧ����Ϣ���沢���ӵ���Ϣ��������Ent��
    i = 1
    while i < 7:
        print(nums[i])
        pe(nums[i])
        print(nums[i])
        Gini_attr(nums[i])
        print(nums[i])
       # print(labels[i], "�Ļ���ֵΪ��", nums[i])
        #Gini.append(Gini_attr(nums[i]))
#        print(labels[i], "�Ļ���ֵΪ��", Gini[i])
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

    min = 1000 # ��ʼ����min��
    m = 0 # m���ڼ�¼min��λ��
    for i in range(1, 6):
        if Gini_i[i] < min:
            m = i
            min = Gini_i[i]
        i = i + 1

    print("ѡ���", m, "�����ԣ���", labels[m], "����Ϊ�������ԣ������ϵ��Ϊ��Gini_i[m] = ", Gini_i[m])