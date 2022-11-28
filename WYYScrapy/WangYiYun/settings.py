# -*- coding: utf-8 -*-
env = 'prod'    # prod/test

from fake_useragent import UserAgent

ua = UserAgent()

if env == 'prod':
    BOT_NAME = 'singers'
    SPIDER_MODULES = ['WangYiYun.spiders']
    NEWSPIDER_MODULE = 'WangYiYun.spiders'
    ROBOTSTXT_OBEY = False

    DEFAULT_REQUEST_HEADERS = {
        "Referer": "http://music.163.com",
        "User-Agent": ua.random
    }

    DOWNLOAD_DELAY = 2
    RANDOMIZE_DOWNLOAD_DELAY = True
    COOKIES_ENABLED = True

    ITEM_PIPELINES = {
        'WangYiYun.pipelines.WangyiyunPipeline': 10,
    }
    '''mongodb://{username}:{password}@{host}:{port}/?authSource={info_data}'''
    MONGODB_HOST = ''
    MONGODB_PORT = int
    MONGODB_USER = ''
    MONGODB_PSW = ''
    MONGODB_DBNAME = 'WangYiYun'
    MONGODB_COL_SONG = 'SongInfo'       # collection
    MONGODB_COL_ALBUM = 'AlbumInfo'
    MONGODB_COL_ALBUMLIST = 'AlbumListInfo'
    MONGODB_COL_ARTIST = 'ArtistInfo'
    MONGODB_COL_COMMENT = 'CommentInfo'

    # GROUP_IDS = (1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003)
    GROUP_IDS = (1001, 1002, 1003)      # 华语歌手
    # INITIALS = [i for i in range(65, 91)] + [0]  # 字母A~Z和其他
    INITIALS = [-1]  # 热门


elif env == 'test':
    BOT_NAME = 'singers'
    SPIDER_MODULES = ['WangYiYun.spiders']
    NEWSPIDER_MODULE = 'WangYiYun.spiders'

    ROBOTSTXT_OBEY = False

    DEFAULT_REQUEST_HEADERS = {
        "Referer": "http://music.163.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }

    ITEM_PIPELINES = {
        'WangYiYun.pipelines.WangyiyunPipeline': 10,
    }

    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DBNAME = 'WYY'
    MONGODB_COL_SONG = 'SongInfo'
    MONGODB_COL_ALBUM = 'AlbumInfo'
    MONGODB_COL_ALBUMLIST = 'AlbumListInfo'
    MONGODB_COL_ARTIST = 'ArtistInfo'
    MONGODB_COL_COMMENT = 'CommentInfo'

    HTTPCACHE_ENABLED = True
    HTTPCACHE_EXPIRATION_SECS = 0
    HTTPCACHE_DIR = 'httpcache'
    HTTPCACHE_IGNORE_HTTP_CODES = []
    HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

    GROUP_IDS = (1001,)
    INITIALS = [-1]