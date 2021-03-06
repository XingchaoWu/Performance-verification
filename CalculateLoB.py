# _*_ coding=utf-8 _*_
# author: xingchaowu
# date: 2020-09-10


import pandas as pd
from scipy import stats
import re
import math


def calculate_blank(data_list):
    # 判断数据是否符合正态分布
    # 读取测试结果（结果按列整理在txt文件中）并存入列表中
    data = open(r"E:\New_Project\05_空白限与检测限计算\demo.txt")
    for d in data.readlines():
        if not d.startswith("#"):
            for i in d.split():
                data_list.append(float(i))
    print(data_list)
    df = pd.DataFrame(data_list,columns=["values"])
    # 正态分布判定
    data_mean = df["values"].mean()  # 计算平均数
    data_std = df["values"].std()  # 计算标准差
    result = stats.kstest(df["values"],"norm",(data_mean,data_std))  # p-value > 0.05 即符合正态分布
    p_value = float(re.findall(r'0.\d+',str(result))[1])  # 提取K-Stest正态检验计算的P值
    if p_value > 0.05:  # 判断是否符合正态分布并返回P值
        print("该数据符合正态分布,p-value:{}".format(p_value))
    else:
        print("该数据不符合正态分布,p-value:{}".format(p_value))

    # 空白值计算
    if p_value > 0.05:
        print("该数据符合正态分布")
        k = eval(input("请输入空白样本数:"))
        blank_cp = 1.645 / (1 - (1/(4*(len(data_list)-k))))
        LoB = data_mean + blank_cp * data_std  # LoB = M + cp * SD
        print("计算的LoB值:{}".format(LoB))
    else:
        print("该数据不符合正态分布")
        data_sorted_list = sorted(data_list)
        Rank_position = len(data_list) * (95 / 100) + 0.5
        LoB =data_sorted_list[int(Rank_position)] \
             + (Rank_position - int(Rank_position)) \
             * (data_sorted_list[math.ceil(Rank_position)]
                - data_sorted_list[int(Rank_position)])  # LoB = X(R) + 0.5(X(R+1)-X(R))
        print("计算的LoB值:{}".format(LoB))


if __name__ == '__main__':
    data_list = []
    calculate_blank(data_list)
