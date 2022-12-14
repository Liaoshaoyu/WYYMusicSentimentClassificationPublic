# -*- coding: utf-8 -*-
import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
from WangYiYun.items import WYYCommentItem


class WangyiyunPipeline(object):
    def __init__(self):
        link = 'mongodb://{username}:{password}@{host}:{port}/?authSource={info_data}'.format(
            username=settings['MONGODB_USER'], password=settings['MONGODB_PSW'], host=settings['MONGODB_HOST'],
            port=settings['MONGODB_PORT'], info_data=settings['MONGODB_DBNAME']
        )
        client = pymongo.MongoClient(link)
        # client = pymongo.MongoClient(
        #     hots=settings['MONGODB_HOST'],
        #     port=settings['MONGODB_PORT'],
        #     username=settings['MONGODB_USER'],
        #     password=settings['MONGODB_PSW'],
        #     authSource=settings['MONGODB_DBNAME']
        # )
        db_name = settings['MONGODB_DBNAME']
        self.db = client[db_name]
        self.artist = self.db[settings['MONGODB_COL_COMMENT']]
        # 不能同时生成多个，只能通过isinstance的方法判断
        # self.album = db[settings['MONGODB_COL_ALBUM']]
        # self.album_list = db[settings['MONGODB_COL_ALBUMLIST']]
        # self.song = db[settings['MONGODB_COL_SONG']]

    def process_item(self, item, spider):
        '''不同的item类型，放入不同的集合中，
        
        分为四块：Items - col - dict - desc ：
            WYYArtistItem - > self.aritst - > artist_infos -> 所有的歌手列表
            WYYAlbumItem - > self.ablum - > album_infos - > 每个歌手的所有专辑列表
            WYYAlbumListItem - > self.album_list - > album_list_infos - > 每张专辑内的所有歌曲列表
            WYYSongItem - > self.song -> song_infos -> 每首歌曲的信息
        '''
        # if isinstance(item, WYYArtistItem):
        #     artist_infos = dict(item)
        #     self.artist.insert_one(artist_infos)
        #     print('WYYArtistItem - > success')
        #
        # if isinstance(item, WYYAlbumItem):
        #     album_infos = dict(item)
        #     self.artist = self.db[settings['MONGODB_COL_ALBUM']]
        #     self.artist.insert_one(album_infos)
        #     print('WYYAlbumItem - > success')
        #
        # if isinstance(item, WYYAlbumListItem):
        #     album_list_infos = dict(item)
        #     self.artist = self.db[settings['MONGODB_COL_ALBUMLIST']]
        #     self.artist.insert_one(album_list_infos)
        #     print('WYYAlbumListItem - > success')
        #
        # if isinstance(item, WYYSongItem):
        #     song_infos = dict(item)
        #     self.artist = self.db[settings['MONGODB_COL_SONG']]
        #     self.artist.insert_one(song_infos)
        #     print('WYYSongItem - > success')

        if isinstance(item, WYYCommentItem):
            comment_infos = dict(item)
            self.artist = self.db[settings['MONGODB_COL_COMMENT']]
            self.artist.insert_one(comment_infos)
            print('WYYCommentItem - > success')

        return item
