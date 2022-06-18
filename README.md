# **情感分析模型使用说明**
```
环境配置：

python3 + tensorflow 2.8.0

本项目所有代码已上传至Github，你可以通过以下指令创建一个conda环境并自己运行一个sensecall项目：

conda create -n sensecall python=3.10 scipy pyyaml jupyter matplotlib
source activate sensecall
conda install tensorflow=2.8.0
git clone git@github.com:KITKATXU/sensecall.git
cd sensecall
git checkout sensecall # switch your branch from 'master' to the 'sensecall'
git submodule init
git submodule update

```



**主要文件说明**

| 运行模块     | 文件名                                             | 文件功能               |
| :----------- | -------------------------------------------------- | ---------------------- |
| **爬虫文件** | **test\get_comment.py**                            | 话题爬取及评论爬取代码 |
|              | **comment\url.csv**                                | 爬虫结果               |
| **数据处理** | **dataProcessing.py**                              | 数据转换代码           |
| **Bert**     | **chinese_L-12_H-768_A-12**                        | 预训练的模型           |
|              | **bert\bert-master\pre_news.py**                   | 数据切分代码           |
|              | **bert\bert-master\qgfl_model**                    | 训练结果               |
|              | **bert\bert-master\mymodel\test_results.tsv**      | 测试结果               |
|              | **bert\bert-master\mymodel\pre_sample.csv**        | 重排结果               |
|              | **bert\bert-master\run_classifier.py**             | 训练及测试部分代码     |
|              | **bert\bert-master\get_results.py**                | j结果转化代码          |
|              | **bert\text-classfication-dataset\data.train.txt** | 训练集                 |
|              | **bert\text-classfication-dataset\data.dev.txt**   | 验证集                 |
|              | **bert\text-classfication-dataset\data.test.txt**  | 测试集                 |



#### **第一步 爬虫代码使用说明：**

1. **爬取当天微博热搜话题**


**打开test/get_comment.py，更改为自己的cookie及user-agent并运行,更改示例：**

```
headers = {
            "Cookie": "_T_WM=50116707496; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1643878787,1643886820,1643889148; SCF=Am2rYpDFDwdVLW6K20J9kESyETHv9-9ovWecPggEfuUwm-4lFGOIykaoJnU8sJfdyQLX4ur57hDdiQWrxbr1biU.; SUB=_2A25M_5PpDeRhGeNI7FoV9irEwj6IHXVsAz2hrDV6PUNbktCOLRH3kW1NSDrv_nFGBHYhFdiXAdRvNgn8Y6McdoKc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJGJBKjv59nMSO1YwICkih5JpX5KzhUgL.Fo-cS0nXSoBR1Kz2dJLoIEBLxK.LB-BL1h-LxK-L122L1-zLxK-LB.-L1K5LxK-LBKML1K5t; SSOLoginState=1643897785; ALF=1646489785; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1643897826 referer: https://weibo.cn/cctvxinwen",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
```

**爬取结果（热门话题及对应话题讨论页url）：**




2. **输入关键词筛选话题，并爬取该话题下评论所有用户的基本信息：**

**'评论者主页', '评论者昵称', '评论者性别', '评论者所在地', '评论者微博数', '评论者关注数', '评论者粉丝数', '评论内容', '评论获赞数', '评论发布时间'。**

**原始评论数据以csv文件形式存储至comment文件夹下，并以评论网页url命名。**

**爬虫实例：**


**存储爬取结果：**




#### **第三步 微博评论情绪重排代码使用说明：**

#### **Training, Testing**

| **Model**      | **example of config file**           | **training & testing** |
| -------------- | ------------------------------------ | ---------------------- |
| **qgfl_model** | **model.ckpt-0.data-00000-of-00001** | **run_classifier.py**  |

1. **切分训练集和测试集**

   **经数据处理后的文件以 ! 分割，从前往后分别是：ID，情绪分数，情绪类别，评论内容**

   **运行 pre_news.py，切分原始文件分别做train，test，dev**

   **切分代码具体过程：先将数据集按8：2切分，8份给train，再从2份里面对半切给test和dev**

2. **训练模型并利用模型计算各情绪类别分值**

**编辑配置文件：**

```
--data_dir=../data
\
--task_name=qgfl
\
--vocab_file=../chinese_L-12_H-768_A-12/vocab.txt
\
--bert_config=../chinese_L-12_H-768_A-12/bert_config.json
\
--output_dir=qgfl_model
\
--do_train=true
\
--do_eval=true
\
--init_checkpoint=../chinese_L-12_H-768_A-12/bert_model.ckpt
\
--max_seq_length=150
\
--train_batch_size=32
\
--learning_rate=5e-5
\
--num_train_epochs=1
\
```

**在终端运行以下命令训练Bert模型：**

```
python run_classifier.py --task_name=qgfl --do_train=true --do_eval=true --do_predict=false --data_dir=../toutiao-text-classfication-dataset-master  --task_name=qgfl  --vocab_file=../chinese_L-12_H-768_A-12/vocab.txt  --bert_config_file=../chinese_L-12_H-768_A-12\bert_config.json  --output_dir=qgfl_model  --do_train=true  --do_eval=true  --init_checkpoint=../chinese_L-12_H-768_A-12/bert_model.ckpt  --max_seq_length=150  --train_batch_size=32  --learning_rate=5e-5  --num_train_epochs=1
```

**在终端运行以下命令对测试数据进行预测分析：**

```
python run_classifier.py   --task_name=qgfl   --do_predict=true   --data_dir=$DATA_DIR   --vocab_file=$BERT_BASE_DIR/vocab.tx
t   --bert_config_file=$BERT_BASE_DIR/bert_config.json   --init_checkpoint=$TRAINED_CLASSIFIER   --max_seq_length=512   --output_dir=./mymodel
```

**可以保存一个.sh来保存训练的命令**

**测试结果存储至mymodel/test_results.tsv**


3. **转化结果进行最终评论重排**

**预测结果test_results.tsv，每一列表示这一行的样本是这一类的概率。将每一列概率与对应类别分值相乘之和即为重排时该条评论的对应情绪分数**

**计算所有测试集评论的情绪积极性分数并按其分数高低存储至mymodel/pre_sample.csv，运行结果转化脚本：**

```
get_results.py
```

