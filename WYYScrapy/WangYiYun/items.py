# -*- coding: utf-8 -*-
import scrapy


class WYYArtistItem(scrapy.Item):
    '''获取所有歌手url
    '''
    _id = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    aritst_url = scrapy.Field()
    album_url = scrapy.Field()


class WYYAlbumListItem(scrapy.Item):
    _id = scrapy.Field()
    album_id = scrapy.Field()
    album_url = scrapy.Field()
    album_list_info = scrapy.Field()


class WYYAlbumItem(scrapy.Item):
    '''专辑的所有歌列表
    '''
    _id = scrapy.Field()
    album_id = scrapy.Field()
    album_url = scrapy.Field()
    album_info = scrapy.Field()
    album_comment_count = scrapy.Field()
    album_comment_info = scrapy.Field()

class WYYSongItem(scrapy.Item):
    '''每首歌信息
    '''
    _id = scrapy.Field()
    song_id = scrapy.Field()
    song_url = scrapy.Field()
    lyric = scrapy.Field()
    song_info = scrapy.Field()
    song_comments = scrapy.Field()
    song_comment_count = scrapy.Field()

class WYYCommentItem(scrapy.Item):
    '''每首歌信息
    '''
    _id = scrapy.Field()
    comment_id = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    time_str = scrapy.Field()
    song_id = scrapy.Field()
    song_name = scrapy.Field()
    classify_by = scrapy.Field()
    positive = scrapy.Field()
    deleted = scrapy.Field()




