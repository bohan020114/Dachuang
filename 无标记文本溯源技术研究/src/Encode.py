import pandas as pd
import numpy as np
import xpinyin as xpy
import jieba
import bch

class EncodeModule:
    def __init__(self):
        None

    def Load(self, txt_path, num, serialLength, dics):
        """
        param:
            txt_path:       文本路径
            num:            待嵌入水印
            serialLength:   嵌入水印位数
            dics:           词典
        """
        self.dic_index = {'B':0, 'C':0, 'D':0, 'T':0, 'E':0, 'F':0,
                          'P':1, 'G':1, 'N':1, 'W':1, 'S':1, 'O':1,
                          'R':2, 'M':2, 'X':2, 'J':2, 'A':2, 'Y':2, 'I':2,
                          'K':3, 'Q':3, 'H':3, 'L':3, 'Z':3, 'U':3, 'V':3}
        self.serialNum = [] # 最终嵌入的水印
        self.ConvertIntoBinary(num, serialLength)
        self.dics = []
        for dic_path in dics:
            dic = pd.read_csv(dic_path, names=[0, 1]) 
            self.dics.append(dic)
        self.txt = list(jieba.cut(open(txt_path, mode="r", encoding="utf-8").read())) # 分词，按行隔开

    def find(self, word, col, dic):
        for i in range(len(dic)):
            if dic[col][i] == word: # 当前编码正确，不替换
                return word, True
            if dic[1-col][i] == word: # 当前编码不正确，替换
                return dic[col][i], True
        return None, False

    def Insert(self):
        py = xpy.Pinyin()
        positions = [0, 0, 0, 0]
        len_serialNum = len(self.serialNum)
        comma_flag = True
        for i in range(len(self.txt)):
            word = self.txt[i]        
            if self.txt[i] == ',':
                self.txt[i] = '，'                           
            if self.txt[i] == '，' and comma_flag == True:            # 当前处于插入逗号状态
                self.txt[i] = ','
                positions = [0, 0, 0, 0]
                comma_flag = False
            elif comma_flag == False and word >= u'\u4e00' and word <= u'\u9fa5':   # 汉字
                first = py.get_initial(word[0])                           # word的首字母
                index = positions[self.dic_index[first]]
                if index == len_serialNum:
                    continue
                col = self.serialNum[index]    # 当前嵌入的01值
                dic = self.dics[self.dic_index[first]]                         # 词典
                chg, flag = self.find(word, col, dic) 
                if flag is True:
                    self.txt[i] = chg # 替换
                    positions[self.dic_index[first]] += 1
                    if positions[self.dic_index[first]] == len_serialNum:
                        tmp = False
                        for i in positions:
                            if i != len_serialNum:
                                tmp = True
                                break
                        if tmp == False:
                            comma_flag = True

    def ConvertIntoBinary(self, num, serialLength):
        """
        把待嵌入的水印num转化为bch加密后的15位二进制数，存放在self.serialNum列表中
        """
        binary = []
        while num:
            if num % 2 == 0:
                binary.insert(0, 0)
            else:
                binary.insert(0, 1)
            num = num // 2
        while len(binary) != serialLength:
            binary.insert(0, 0)
        self.serialNum = bch.bchEncode(np.array(binary)).tolist()

    def InsertWatermark(self, out_path):
        self.Insert()
        fout = open(out_path, mode="w", encoding="utf-8")
        for i in self.txt:
            fout.write(i)
        fout.close()
               
        