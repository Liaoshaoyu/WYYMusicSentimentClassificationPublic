import time
from collections import Counter
from datetime import datetime, timedelta

import jieba
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from config import Config
from dataBase.mongodb import MongoDB
import numpy as np

mdb = MongoDB()


class ColUpdate:
    def content_length_handle(self) -> None:
        col = mdb.make_col('CommentInfo')
        result = col.aggregate([
            {'$match': {
                'deleted': 0
            }},
            {'$project': {
                '_id': 0,
                "content_len": {'$strLenCP': "$content"}
            }}
        ])

        def find_index(num):
            if num > Config.BINS[-1]:
                return -1
            r = len(Config.BINS)
            l = 0
            while l <= r:
                mid = (l + r) // 2
                if Config.BINS[mid] <= num <= Config.BINS[mid + 1]:
                    return mid
                elif num < Config.BINS[mid]:
                    r = mid - 1
                else:
                    l = mid + 1

        yaxis = [0] * len(Config.LABELS)
        xaxis = Config.LABELS
        for item in result:
            idx = find_index(item['content_len'])
            yaxis[idx] += 1

        content_len_col = mdb.make_col('ContentLength')
        data = {'xaxis': xaxis, 'yaxis': yaxis, 'create_time': datetime.now(), 'deleted': 0}

        content_len_col.insert_one(data)

        # nums = [item['content_len'] for item in result]
        #
        # # 通过seaborn查看直方图
        # nums_df = pd.DataFrame(data=nums, columns=['content_len'])
        # sns.histplot(data=nums_df, x='content_len', bins=10, kde=True)
        # plt.show()
        #
        # # 组距=方差/组数，然后向上取整
        # nums = np.asarray(nums)

    def word_cloud_handle(self) -> None:
        col = mdb.make_col('CommentInfo')
        str_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
        s_t = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")  # 返回元祖
        today = int(time.mktime(s_t) * 1000)

        str_time = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d 00:00:00")
        s_t = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")  # 返回元祖
        ytd = int(time.mktime(s_t) * 1000)

        result = col.aggregate([
            {'$match': {
                'deleted': 0,
                'time': {'$gte': ytd, '$lt': today}
            }},
            {'$project': {
                '_id': 0,
                "content": 1
            }}
        ])

        # 停用词
        with open('Chinese_English_stopwords.txt', mode='r') as f:
            stop_words = f.read().split('\n')
        with open('cn_stopwords.txt', mode='r') as f1:
            stop_words1 = f1.read().split('\n')
        my_stop_words = ['，', '的', ' ', '我', '了', '你', '。', '是', '[', ']', '\n', '在', '不', '！', '都', '也', '人',
                         '就', '\u200b', '这', '和', '我们', '?', '？']
        for sw, msw in zip(stop_words1, my_stop_words):
            stop_words.append(sw)
            stop_words.append(msw)
        words = []
        for item in result:
            word = jieba.lcut(item['content'])
            for w in word:
                if w not in stop_words:
                    words.append(w)
        words_cnt = Counter(words)

        # 更新词云
        word_cloud_col = mdb.make_col('WordCloud')
        result = word_cloud_col.aggregate([
            {'$match': {
                'deleted': 0
            }},
            {'$sort': {'create_time': -1}},
            {'$limit': 1},
            {'$project': {
                '_id': 0,
                "word_cloud": 1
            }}
        ])
        old_word_cloud = []
        for r in result:
            old_word_cloud.append(r)
        if old_word_cloud:
            old_word_cloud = old_word_cloud[0]['word_cloud']
            new_word_cloud = Counter(old_word_cloud) + words_cnt
            word_cloud_col.insert_one({'word_cloud': new_word_cloud, 'create_time': datetime.now(), 'deleted': 0})
        else:
            word_cloud_col.insert_one({'word_cloud': words_cnt, 'create_time': datetime.now(), 'deleted': 0})
