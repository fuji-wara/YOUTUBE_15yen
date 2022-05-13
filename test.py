from pymongo import MongoClient
import csv
# mongo 設定
client = MongoClient('localhost', 27017) # ローカルホストDBに接続。

collection1 = client.YOUTUBE.channel_list1
collection2 = client.YOUTUBE.completion_list



for i in collection2.find():
    print(i['チャンネル名'])
