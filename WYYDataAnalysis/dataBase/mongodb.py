import pymongo

class MongoDB:
    def __init__(self):
        db_url = 'mongodb://{username}:{password}@{host}:{port}/?authSource={info_data}'
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client['WangYiYun']


    def make_col(self, collection_name: str):

        return self.db[collection_name]


