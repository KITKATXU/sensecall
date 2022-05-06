import os
import pandas as pd
import numpy as np

if __name__ == '__main__':
    path = "mymodel"
    pd_all = pd.read_csv(os.path.join(path, "test_results.tsv"), sep='\t', header=None)
    pd_txt = pd.read_csv("C:\\Users\\Administrator\\Desktop\\pinglun\\bert\\toutiao-text-classfication-dataset-master\\toutiao_cat_data.test.txt", sep='\t', header=None)
    f = open(
        'C:\\Users\\Administrator\\Desktop\\pinglun\\bert\\toutiao-text-classfication-dataset-master\\toutiao_cat_data.test.txt',
        'r', encoding='utf-8')
    test_data = []
    index = 0



    data = pd.DataFrame(columns=['result', 'text'])
    pd_all = pd_all.iloc[:, :5]
    print(pd_all.shape)
    labels = ["评分 150  情绪类别 愤怒",
              "评分 350  情绪类别 积极",
              "评分 187  情绪类别 无情绪",
              "评分  50  情绪类别 悲伤",
              "评分 225  情绪类别 惊奇",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极",
              "评分 350  情绪类别 积极"]
    index=0
    for line in f.readlines():
        guid = "dev-%d" % (index)
        line = line.replace('\n', '').split('_!_')
        data.loc[index , 'text']=line[3]
        index=index+1
    for index in pd_all.index:
        sum_tst = 0
        sum_tst = sum_tst + pd_all.loc[index].values[0] * 150 + pd_all.loc[index].values[1] * 350 + \
                  pd_all.loc[index].values[2] * 187 + pd_all.loc[index].values[3] * 50 + pd_all.loc[index].values[
                      4] * 225

        data.loc[index ,'result'] = sum_tst
    data.sort_values(by="result", inplace=True, ascending=False)
    data.to_csv(os.path.join(path, "pre_sample.csv"), sep=',',encoding='utf-8-sig')
    print(data)
