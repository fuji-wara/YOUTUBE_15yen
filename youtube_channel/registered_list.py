from selenium.webdriver import Chrome, ChromeOptions
from pymongo import MongoClient
import os
from csv import DictWriter
import csv


# mongo 設定
client = MongoClient('localhost', 27017) # ローカルホストDBに接続。
collection1 = client.YOUTUBE.registered_channels
collection1.create_index('key', unique = True) # データを一意に識別するキーを格納するkeyフィールドにユニークなインデックを作成する。

pas = '/Users/fujiwarayuuki/お仕事お仕事/CSV/チャンネルリサーチ除外一覧表 - リサーチ除外一覧表.csv'

with open(pas, 'r') as ff:
    reader = csv.DictReader(ff)
    z = [row for row in reader]

for i in z :
    key = i['チャンネル名']
    url = i['チャンネルURL']
    dict = {'url':url, 'key':key, 'video':'aaaa' }
    manga = collection1.find_one({'key': key})
    if not manga:

        collection1.insert_one(dict)
        print('成功')
    else:
        print('被り')
