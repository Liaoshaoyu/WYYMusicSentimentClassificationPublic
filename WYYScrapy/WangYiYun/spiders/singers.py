# -*-coding:utf-8-*-
from __future__ import absolute_import
import re
import requests

import scrapy
from scrapy import cmdline
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
from WangYiYun.items import WYYArtistItem, WYYAlbumListItem, WYYAlbumItem, WYYSongItem, WYYCommentItem
from WangYiYun.spiders.CommentCrawl import CommentCrawlClass


# from CommentCrawl import CommentCrawlClass


class WangYiYunCrawl(scrapy.Spider):
    name = 'singers'
    allowed_domains = ['music.163.com']
    # self.start_urls = 'http://music.163.com/discover/artist/cat?id={gid}&initial={initial}'

    group_ids = settings.get('GROUP_IDS')
    initials = settings.get('INITIALS')

    headers = {
        "Referer": "http://music.163.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        for gid in self.group_ids:
            for initial in self.initials:
                url = 'http://music.163.com/discover/artist/cat?id={gid}&initial={initial}'.format(
                    gid=gid, initial=initial
                )
                yield scrapy.Request(url=url, headers=self.headers, method='GET', callback=self.parse)

    def parse(self, response, **kwargs):
        lis = response.selector.xpath('//ul[@id="m-artist-box"]/li')
        for li in lis:
            post_urls = li.xpath('//a[@class="nm nm-icn f-thide s-fc0"]/@href').extract()
            for post_url in post_urls:
                # print(post_url)     # /artist?id=48568460
                item = WYYArtistItem()
                p_url = post_url.lstrip()
                # print(p_url)     # /artist?id=48568460
                album_url = p_url.split('?')
                # print(album_url)        # ['/artist', 'id=46956087']
                item['artist_id'] = int(re.compile(r'\d+').findall(p_url)[0])
                item['aritst_url'] = 'http://music.163.com' + p_url
                item['album_url'] = 'http://music.163.com' + album_url[0] + '/album?' + album_url[1]
                item['artist_name'] = li.xpath('//a[@class="nm nm-icn f-thide s-fc0"]/text()').extract()[0]
                yield scrapy.Request(url=item['album_url'], headers=self.headers, method='GET',
                                     callback=self.parse_album_list)

    def get_album_list_page(self, response):
        '''判断http://music.163.com/artist/album?id=xx页的专辑有多少页，如果标签不在，则返回1
        '''
        page = response.selector.xpath('//a[@class="zpgi"]/text()').extract()
        if page:
            page = int(page[-1])
        else:
            page = 1
        return page

    def parse_album_list(self, response):
        item = WYYAlbumListItem()
        # print(response.url)     # https://music.163.com/artist/album?id=12084497
        params = response.url.split('?')[-1]
        params = params.split('&')
        singer_id = ''
        for p in params:
            if 'id' in p:
                singer_id = p.split('=')[-1]

        item['album_id'] = singer_id
        item['album_url'] = response.url
        page_count = self.get_album_list_page(response)
        album_list = self.get_artist_album_info(singer_id, page_count)
        item['album_list_info'] = album_list
        for albums in album_list:
            hotAlbums = albums['hotAlbums']
            for hot_album in hotAlbums:
                album_id = hot_album['id']
                album_url = 'http://music.163.com/album?id=' + str(album_id)
                yield scrapy.Request(url=album_url, headers=self.headers, method='GET', callback=self.parse_album)

    def parse_album(self, response):
        # item = WYYAlbumItem()
        # print(response.url)     # 'https://music.163.com/album?id=122706076'
        params = response.url.split('?')[-1]
        params = params.split('&')
        album_id = ''
        for p in params:
            if 'id' in p:
                album_id = p.split('=')[-1]

        # comment_url = 'http://music.163.com/weapi/v1/resource/comments/R_AL_3_%s?csrf_token=' % album_id
        # item['album_id'] = album_id
        # item['album_url'] = response.url

        album_info = self.get_album_info(album_id)
        album = album_info.get('album')
        if album is not None:
            # album_comment_count = album_info['album']['info']['commentCount']
            # item['album_info'] = album_info
            # item['album_comment_count'] = album_comment_count

            # comment_url: 'http://music.163.com/weapi/v1/resource/comments/R_AL_3_154372290?csrf_token='
            # album_comment_count: 2799
            # comment_craw = CommentCrawlClass(comment_url)
            # item['album_comment_info'] = comment_craw.get_album_comment(album_comment_count)

            songs = album_info['album']['songs']
            if songs:
                for song in songs:
                    song_id = song['id']
                    song_url = 'http://music.163.com/song?id=' + str(song_id)
                    # yield scrapy.Request(url=song_url, headers=self.headers, method='GET', callback=self.parse_song)
                    yield scrapy.Request(url=song_url, headers=self.headers, method='GET', callback=self.parse_comment)

    # def parse_song(self, response):
    #     item = WYYSongItem()
    #     params = response.url.split('?')[-1]
    #     params = params.split('&')
    #     song_id = ''
    #     for p in params:
    #         if 'id' in p:
    #             song_id = p.split('=')[-1]
    #
    #     item['song_id'] = song_id
    #     comment_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=' % song_id
    #     item['song_url'] = response.url
    #     item['lyric'] = self.get_lyric(song_id)
    #     item['song_info'] = self.get_song_info(song_id)
    #
    #     comment_craw = CommentCrawlClass(comment_url)
    #     item['song_comments'] = comment_craw.get_song_comment()
    #     yield item

    def parse_comment(self, response):
        item = WYYCommentItem()
        params = response.url.split('?')[-1]
        params = params.split('&')
        song_id = ''
        for p in params:
            if 'id' in p:
                song_id = p.split('=')[-1]

        item['song_id'] = song_id
        comment_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=' % song_id
        song_info = self.get_song_info(song_id)
        if song_info:
            songs = song_info.get('songs')
            if songs:
                item['song_name'] = songs[0].get('name')
            else:
                item['song_name'] = 'unknow'

        comment_craw = CommentCrawlClass(comment_url)
        song_comments = comment_craw.get_song_comment()
        if song_comments:
            for sc in song_comments:
                comments = sc.get('comments')
                if comments is not None:
                    for c in comments:
                        item['comment_id'] = c.get('commentId')
                        item['content'] = c.get('content')
                        item['time'] = c.get('time')
                        item['time_str'] = c.get('timeStr')
                        item['classify_by'] = None
                        item['positive'] = None
                        item['deleted'] = 0

                        yield item

    def get_req(self, url, params=None):
        try:
            req = requests.get(url, headers=self.headers, params=params)
            return req
        except Exception as e:
            with open('error_url.txt', 'a+') as f:
                f.write(url + '\n')
            print(url, e)
            return None

    def get_artist_album_info(self, singer_id, page_count):
        album_list = []
        albums_url = 'http://music.163.com/api/artist/albums/%s' % singer_id
        for offset in range(0, page_count):
            params = {
                'id': singer_id,
                'offset': offset * 12,
                'total': 'true',
                'limit': 12
            }
            # print(albums_url)       # http://music.163.com/api/artist/albums/1203045
            resp = self.get_req(albums_url, params=params)
            data = resp.json()
            album_list.append(data)
        return album_list

    def get_album_info(self, album_id):
        songs_url = 'http://music.163.com/api/album/%s?ext=true&id=%s&offset=0&total=true' % (album_id, album_id)
        # print(songs_url)        # http://music.163.com/api/album/153596671?ext=true&id=153596671&offset=0&total=true
        req = self.get_req(songs_url)
        if req.status_code == 200:
            return req.json()

    def get_song_info(self, song_id):
        # param = urlencode({'id':%s,'ids':[%s]}) % (song_id,song_id)
        song_url = 'http://music.163.com/api/song/detail/?id=%s&ids=[%s]' % (song_id, song_id)
        req = self.get_req(song_url)
        if req.status_code == 200:
            return req.json()

    def get_lyric(self, song_id):
        lyric_url = 'http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1' % song_id
        req = self.get_req(lyric_url)
        if req.status_code == 200:
            return req.json()
        else:
            return 'None'


if __name__ == '__main__':
    cmdline.execute("scrapy crawl singers".split())

# if __name__ == '__main__':
#     # 通过方法 get_project_settings() 获取配置信息
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(WangYiYunCrawl)
#     process.start()
