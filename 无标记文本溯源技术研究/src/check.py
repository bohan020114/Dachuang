import jieba

before = list(jieba.cut(open("../datas/before.txt", mode="r", encoding="utf-8").read())) 
after = list(jieba.cut(open("../datas/after.txt", mode="r", encoding="utf-8").read()))
for i, j in zip(before, after):
    if i != j:
        print(f"before: {i}")
        print(f"after: {j}")