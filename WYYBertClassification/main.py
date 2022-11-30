import torch
import torch.optim as optim
from matplotlib import pyplot as plt
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig, AdamW, WarmupLinearSchedule

import json
import numpy as np
import pandas as pd
# import seaborn as sns
import tensorboardX
import os

from predict import Predict

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

# writer = tensorboardX.SummaryWriter('/root/tf-logs')

# 超参数
EPOCHS = 5  # 训练的轮数
BATCH_SIZE = 32  # 批大小
MAX_LEN = 300  # 文本最大长度
LR = 1e-5  # 学习率
# WARMUP_STEPS = 100  # 热身步骤
# T_TOTAL = 1000  # 总步骤
MODEL_SAVING_PATH = './models/bert_classify.ckpt'

BERT_BASE_CHINESE_PATH = 'bert-base-chinese'
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print('device: ', device)
print('gpu_nums: ', torch.cuda.device_count())

# BERT_BASE_CHINESE_PATH = './bert-base-chinese'
# device = torch.device('mps')
# print('device: ', device)

tokenizer = BertTokenizer.from_pretrained(BERT_BASE_CHINESE_PATH)
# tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
print('tokenizer is ready.')


# pytorch的dataset类 重写getitem,len方法
class Custom_dataset(Dataset):
    def __init__(self, dataset_list):
        self.dataset = dataset_list

    def __getitem__(self, index):
        text = str(self.dataset[index][0])
        label = str(self.dataset[index][1])

        return text, label

    def __len__(self):
        return len(self.dataset)


# 加载数据集
def load_dataset(df: pd.DataFrame, max_len):
    # 根据max_len参数进行padding
    json_file = json.loads(df.to_json(orient='records'))
    data_list = []
    for jf_item in json_file:
        content = jf_item['CONTENT']
        label = jf_item['label']
        content = content.replace(' ', '')
        content = tokenizer.encode(content)
        num = max_len - len(content)
        if num < 0:
            # 在开头和结尾加[CLS] [SEP]
            content = content[:max_len]
        else:
            content = content + [0] * num
        # 在开头和结尾加[CLS] [SEP]
        content = [101] + content[:max_len] + [102]
        if len(content) == max_len + 2 and isinstance(label, int):
            data_list.append([content, label])

    return data_list


# 计算每个batch的准确率
def batch_accuracy(pre, label):
    pre = pre.argmax(dim=1)
    correct = torch.eq(pre, label).sum().float().item()
    accuracy = correct / float(len(label))

    return accuracy


def train() -> BertForSequenceClassification:
    train_df = pd.read_csv('data/comment_trainset_2class.csv')
    train_df['label'] = train_df['label'].apply(lambda x: 0 if x == -1 else x)

    # 生成数据集以及迭代器
    train_dataset = load_dataset(train_df, max_len=MAX_LEN)
    train_cus = Custom_dataset(train_dataset)
    train_loader = DataLoader(dataset=train_cus, batch_size=BATCH_SIZE, shuffle=True)
    print('数据集加载完毕！')

    # Bert模型以及相关配置
    config = BertConfig.from_pretrained(BERT_BASE_CHINESE_PATH)
    config.num_labels = 2
    print('BertConfig加载完毕！')

    model = BertForSequenceClassification.from_pretrained(BERT_BASE_CHINESE_PATH, config=config)
    model = model.to(device)
    print('BertModel加载完毕！')

    optimizer = AdamW(model.parameters(), lr=LR, correct_bias=False)

    len_dataset = len(train_loader)
    total_steps = (len_dataset // BATCH_SIZE) * EPOCHS if len_dataset % BATCH_SIZE == 0 else (
                                                                                                         len_dataset // BATCH_SIZE + 1) * EPOCHS  # 每一个epoch中有多少个step可以根据len(DataLoader)计算：total_steps = len(DataLoader) * epoch
    warmup_step = int(total_steps * 0.1)
    print(f'totol_step: {total_steps}, warmup_step: {warmup_step}')
    scheduler = WarmupLinearSchedule(optimizer, warmup_steps=warmup_step, t_total=total_steps)
    # optimizer = optim.Adam(model.parameters(), lr=LR)

    model.train()
    print('开始训练...')
    for epoch in range(EPOCHS):
        for i, data in enumerate(train_loader):
            text_list = list(map(json.loads, data[0]))
            label_list = list(map(json.loads, data[1]))

            text_tensor = torch.tensor(text_list).to(device)
            label_tensor = torch.tensor(label_list).to(device)

            outputs = model(text_tensor, labels=label_tensor)
            loss, logits = outputs[:2]
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            acc = batch_accuracy(logits, label_tensor)
            print(
                'epoch:{} | acc:{} | loss:{} | progress: {}/{}'.format(epoch + 1, acc, loss, i + 1, len(train_loader)))

            # writer.add_scalar('train loss', loss.item(), global_step=i)
            # writer.add_scalar('train acc', acc, global_step=i)

        scheduler.step()

    torch.save(model.state_dict(), MODEL_SAVING_PATH)
    print('保存训练完成的model...')

    return model


def test() -> None:
    test_df = pd.read_csv('data/comment_testset_2class.csv')
    test_df['label'] = test_df['label'].apply(lambda x: 0 if x == -1 else x)

    # 通过seaborn查看直方图
    # test_df['content_len'] = test_df['CONTENT'].apply(lambda x: len(x))
    # nums_df = pd.DataFrame(data=test_df, columns=['content_len'])
    # sns.histplot(data=nums_df, x='content_len', bins=10, kde=True)
    # plt.show()

    # 生成数据集以及迭代器
    test_dataset = load_dataset(test_df, max_len=MAX_LEN)
    print('数据集加载完毕！')

    # Bert模型以及相关配置
    config = BertConfig.from_pretrained(BERT_BASE_CHINESE_PATH)
    config.num_labels = 2
    print('BertConfig加载完毕！')

    trained_model = BertForSequenceClassification.from_pretrained(BERT_BASE_CHINESE_PATH, config=config)
    trained_model = trained_model.to(device)
    print('BertModel加载完毕！')

    # 测试=
    print('开始加载训练完成的model...')
    trained_model.load_state_dict(torch.load(MODEL_SAVING_PATH, map_location=device))

    print('开始测试...')
    trained_model.eval()

    tset_cus = Custom_dataset(test_dataset)
    test_loader = DataLoader(dataset=tset_cus, batch_size=BATCH_SIZE, shuffle=False)
    for i, data in enumerate(test_loader):
        text_list = list(map(json.loads, data[0]))
        label_list = list(map(json.loads, data[1]))
        text_tensor = torch.tensor(text_list).to(device)
        label_tensor = torch.tensor(label_list).to(device)

        with torch.no_grad():
            outputs = trained_model(text_tensor, labels=label_tensor)
            loss, logits = outputs[:2]
            acc = batch_accuracy(logits, label_tensor)
            print('test => acc:{} | loss:{} | progress: {}/{}'.format(acc, loss, i + 1, len(test_loader)))

            # writer.add_scalar('test loss', loss.item(), global_step=i)
            # writer.add_scalar('test acc', acc, global_step=i)



if __name__ == "__main__":
    model = train()
    test()
    # writer.close()

    # pre = Predict()
    # pre.predict_handle()
