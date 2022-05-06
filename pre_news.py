import numpy as np

f = open('C:\\Users\\Administrator\\Desktop\\pinglun\\bert\\toutiao-text-classfication-dataset-master\\new_data.txt', 'r', encoding='utf-8')
train_list = []
for line in f.readlines():
    print(line)
    if line == '':
        continue
    train_list.append(line)

train_list = np.array(train_list)

f.close()


def split_train(data, test_ratio):
    np.random.seed(43)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data[train_indices], data[test_indices]


train_data, tdev_data = split_train(train_list, 0.2)

test_data, dev_data = split_train(tdev_data, 0.5)
print(len(train_data), len(test_data), len(dev_data))
# 写入train
file_train = open('C:\\Users\\Administrator\\Desktop\\pinglun\\bert\\toutiao-text-classfication-dataset-master\\new_cat_data.train.txt', 'w', encoding='utf-8')
for i in train_data:
    file_train.write(i)
file_train.close()

# 写入test
file_test = open('C:\\Users\\Administrator\\Desktop\\pinglun\\bert\\toutiao-text-classfication-dataset-master\\new_cat_data.test.txt', 'w', encoding='utf-8')
for i in test_data:
    file_test.write(i)
file_test.close()

# 写入dev
file_dev = open('C:\\Users\\Administrator\\Desktop\\pinglun\\bert\\toutiao-text-classfication-dataset-master\\new_cat_data.dev.txt', 'w', encoding='utf-8')
for i in dev_data:
    file_dev.write(i)
file_dev.close()

