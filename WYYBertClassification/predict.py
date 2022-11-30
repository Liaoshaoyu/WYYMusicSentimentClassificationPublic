import time
from datetime import datetime, timedelta

import torch
from transformers import BertTokenizer, BertConfig, BertForSequenceClassification

from dataBase.mongodb import MongoDB
from bson import ObjectId

mdb = MongoDB()
MAX_LEN = 300  # 文本最大长度
MODEL_SAVING_PATH = './models/bert_classify.ckpt'
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
BERT_BASE_CHINESE_PATH = './bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(BERT_BASE_CHINESE_PATH)


class Predict:
    @staticmethod
    def predict(content: str) -> int:
        config = BertConfig.from_pretrained(BERT_BASE_CHINESE_PATH)
        config.num_labels = 2
        trained_model = BertForSequenceClassification.from_pretrained(BERT_BASE_CHINESE_PATH, config=config)
        trained_model = trained_model.to(device)
        trained_model.eval()

        content = tokenizer.encode(content)
        num = MAX_LEN - len(content)
        if num < 0:
            # 在开头和结尾加[CLS] [SEP]
            content = content[:MAX_LEN]
        else:
            content = content + [0] * num
        # 在开头和结尾加[CLS] [SEP]
        content = [101] + content[:MAX_LEN] + [102]
        text_tensor = torch.tensor(content).to(device)

        with torch.no_grad():
            outputs = trained_model(text_tensor.view(1, -1), labels=None)

        return outputs[0].argmax(dim=1).item()


    def predict_handle(self) -> None:
        col = mdb.make_col('CommentInfo')
        # str_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
        # s_t = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")  # 返回元祖
        # today = int(time.mktime(s_t) * 1000)
        #
        # str_time = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d 00:00:00")
        # s_t = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")  # 返回元祖
        # ytd = int(time.mktime(s_t) * 1000)

        result = col.aggregate([
            {'$match': {
                'deleted': 0,
                'positive': None
                # 'time': {'$gte': ytd, '$lt': today}
            }}
        ])

        # total = more_itertools.ilen(result)     # 会把result迭代完了
        # total = len(list(result))
        # total = sum(1 for _ in result)

        # for i, item in enumerate(result):
        #     positive = self.predict(item['content'])
        #     positive = True if positive else False
        #     _id = item['_id']
        #     col.update_one({"_id": ObjectId(_id)}, {"$set": {"classify_by": '智能分类', 'positive': positive}})

        result_arr = []
        for item in result:
            result_arr.append({'_id': item['_id'], 'content': item['content']})
        total = len(result_arr)
        print(f'一共{total}条数据需要分类')

        for i, item in enumerate(result_arr):
            content = item['content']
            positive = self.predict(content)
            positive = True if positive else False
            _id = item['_id']
            col.update_one({"_id": ObjectId(_id)}, {"$set": {"classify_by": '智能分类', 'positive': positive}})
            print(f'progress: {i + 1}/{total}|{positive}|{content}')




