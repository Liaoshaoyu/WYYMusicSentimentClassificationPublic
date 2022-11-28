# -*-coding:utf-8-*-
from __future__ import absolute_import
import os
import json
import base64
import time
from datetime import datetime, timedelta

import requests
from Crypto.Cipher import AES


class CommentCrawlClass(object):

    def __init__(self, comment_url):
        self.comment_url = comment_url
        self.headers = {
            "Referer": "http://music.163.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }
        self.ytd_date_str = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    def createSecretKey(self, size):
        '''生成长度为16的随机字符串作为密钥secKey
        '''
        hex_key = map(lambda x: (hex(x)[2:]), os.urandom(16))
        return (''.join(hex_key))[0:16]

    def AES_encrypt(self, text, secKey):
        '''进行AES加密
        '''
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        encrypt_text = encryptor.encrypt(text.encode())
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def rsaEncrypt(self, text, pubKey, modulus):
        '''进行RSA加密
        '''
        text = text[::-1]
        num0 = int(text.encode('utf-8').hex(), 16)
        num1 = int(pubKey, 16)
        num2 = int(modulus, 16)
        rs = num0 ** num1 % num2
        return format(rs, 'x').zfill(256)

    def encrypted_request(self, text):
        '''将明文text进行两次AES加密获得密文encText,
        因为secKey是在客户端上生成的，所以还需要对其进行RSA加密再传给服务端。
        '''
        pubKey = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'

        text = json.dumps(text)
        secKey = self.createSecretKey(16)       # a04b54a70ca30768
        secKey0 = self.AES_encrypt(text, nonce)     # b'd4dGohDH12MPCs+0cSHCv/GTMYMDyO4s151j9ePL/Ry0BPSsaGvgfbaPZK+Wsd4hkb4VocYrnSyEPP7/4U8xcOKhaZ2ObAknB8QPsmqj8C8='
        secKey0 = secKey0.decode()
        encText = self.AES_encrypt(secKey0, secKey)
        encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        return data

    def get_post_req(self, url, data):
        req = requests.post(url, headers=self.headers, data=data)

        return req.json()

    def get_offset(self, offset=0):
        if offset == 0:
            text = {'rid': '', 'offset': '0', 'total': 'true', 'limit': '20', 'csrf_token': ''}
        else:
            text = {'rid': '', 'offset': '%s' % offset, 'total': 'false', 'limit': '20', 'csrf_token': ''}
        return text

    def get_json_data(self, url, offset):
        text = self.get_offset(offset)
        data = self.encrypted_request(text)
        json_text = self.get_post_req(url, data)
        return json_text

    def get_song_comment(self):
        comment_info = []
        data = self.get_json_data(self.comment_url, offset=0)
        comment_count = data['total']
        flag = False
        if comment_count:
            if isinstance(data.get('comments'), list):
                new_comments = []
                for comment_item in data['comments']:
                    time_array = time.localtime(comment_item['time'] / 1000)
                    date_str = time.strftime("%Y-%m-%d", time_array)
                    if date_str == self.ytd_date_str:
                        new_comments.append(comment_item)
                data['comments'] = new_comments
            comment_info.append(data)

            if comment_count > 20:
                for offset in range(20, int(comment_count), 20):
                    comment = self.get_json_data(self.comment_url, offset=offset)
                    if isinstance(comment.get('comments'), list):
                        new_comments = []
                        for comment_item in comment['comments']:
                            time_array = time.localtime(comment_item['time'] / 1000)
                            date_str = time.strftime("%Y-%m-%d", time_array)
                            if date_str == self.ytd_date_str:
                                new_comments.append(comment_item)
                            else:
                                flag = True
                                break
                        comment['comments'] = new_comments
                    comment_info.append(comment)
                    if flag:
                        break

        return comment_info

    def get_album_comment(self, comment_count):
        album_comment_info = []
        if comment_count:
            for offset in range(0, int(comment_count), 20):
                comment = self.get_json_data(self.comment_url, offset=offset)
                album_comment_info.append(comment)
        return album_comment_info
