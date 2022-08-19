import pandas as pd
import xpinyin as xpy

dic = pd.read_csv("./datas/2017.txt", names=[0, 1])
dic_list = []
dic_list.append(open("./datas/dics/0.txt", mode="w", encoding="utf-8"))
dic_list.append(open("./datas/dics/1.txt", mode="w", encoding="utf-8"))
dic_list.append(open("./datas/dics/2.txt", mode="w", encoding="utf-8"))
dic_list.append(open("./datas/dics/3.txt", mode="w", encoding="utf-8"))

relation = {'B':0, 'C':0, 'D':0, 'T':0, 'E':0, 'F':0,
            'P':1, 'G':1, 'N':1, 'W':1, 'S':1, 'O':1,
            'R':2, 'M':2, 'X':2, 'J':2, 'A':2, 'Y':2, 'I':2,
            'K':3, 'Q':3, 'H':3, 'L':3, 'Z':3, 'U':3, 'V':3}

py = xpy.Pinyin()

for i in range(len(dic)):
    fir = py.get_initial(dic[0][i].strip()[0])
    sec = py.get_initial(dic[1][i].strip()[0])
    if relation[fir] == relation[sec]:
        dic_list[relation[fir]].write(f"{dic[0][i].strip()},{dic[1][i].strip()}\n")


