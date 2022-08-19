import numpy as np
import pandas as pd
import xpinyin as xpy
import jieba
import bch

class DecodeModule:
    def __init__(self):
        None

    def Load(self, txt_path, serial_len, dics):
        self.serial_len = serial_len
        self.relation = {'B':0, 'C':0, 'D':0, 'T':0, 'E':0, 'F':0,
                         'P':1, 'G':1, 'N':1, 'W':1, 'S':1, 'O':1,
                         'R':2, 'M':2, 'X':2, 'J':2, 'A':2, 'Y':2, 'I':2,
                         'K':3, 'Q':3, 'H':3, 'L':3, 'Z':3, 'U':3, 'V':3}
        self.dics = []
        for dic_path in dics:
            dic = pd.read_csv(dic_path, header=None, names=[0, 1]) 
            self.dics.append(dic)
        self.txt = list(jieba.cut(open(txt_path, mode="r", encoding="utf-8").read())) # 分词，按行隔开
        self.txt_split = []
        self.Pretreatment()
    
    def Pretreatment(self):
        py = xpy.Pinyin()
        tmp_split_txt = []
        for _ in range(len(self.dics)):
            tmp_split_txt.append([])
        flag = 0
        for word in self.txt:
            if word == ',':
                flag += 1
                if flag == 2:
                    flag = 1
                    self.txt_split.append(tmp_split_txt)
                    for i in range(len(tmp_split_txt)):
                        tmp_split_txt[i] = []
            elif flag == 1 and word >= u'\u4e00' and word <= u'\u9fa5': # word是汉字
                fir = py.get_initial(word[0])
                tmp_split_txt[self.relation[fir]].append(word)
    
    def find(self, word, dic):
        for i in range(len(dic)):
            if dic[0][i] == word: 
                return 0
            if dic[1][i] == word: 
                return 1
        return None

    def Check(self): 
        ans = []   
        for tmp_txt_split in self.txt_split:
            for i in range(len(self.dics)):
                tmp_serialNum = []
                txt = tmp_txt_split[i]
                dic = self.dics[i]
                for word in txt:
                    res = self.find(word, dic) 
                    if res is not None:
                        tmp_serialNum.append(res)
                        if len(tmp_serialNum) == self.serial_len:
                            ans.append(tmp_serialNum)
                            break     
        return ans
    
    def ConvertIntoNumber(self, arr):
        res = []
        for bchcode in arr:
            flag = bch.bchDecode(np.array(bchcode))
            if flag == True:
                num = 0
                num_binary = bchcode[0:7]
                for j in num_binary:
                    if j == 1:
                        num = num * 2 + 1
                    else:
                        num = num * 2
                res.append(num)
        return res

    def Evaluate(self, res):
        convert = self.ConvertIntoNumber(res)
        single = set(convert)
        res_dic = {}
        for i in single:
            arr = [1 if i == j else 0 for j in convert]
            res_dic[i] = sum(arr)
        max = 0
        max_serial = None
        print("The result of decode:")
        for i in res_dic.keys():
            print(f"\t{i} : {res_dic[i]}")
            if res_dic[i] > max:
                max = res_dic[i]
                max_serial = i
        print(f"The most likely serial num is {max_serial}")
