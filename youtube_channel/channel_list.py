

import se as s
from pymongo import MongoClient
from bs4 import BeautifulSoup
import os
import time
from csv import DictWriter
import csv


# mongo 設定
client = MongoClient('localhost', 27017) # ローカルホストDBに接続。
collection1 = client.YOUTUBE.registered_channels
collection1.create_index('key', unique = True) # データを一意に識別するキーを格納するkeyフィールドにユニークなインデックを作成する。

collection2 = client.YOUTUBE.new_channel

search_url = [
    f'https://www.youtube.com/results?search_query=パチンコ&sp=CAESAhAC',
    f'https://www.youtube.com/results?search_query=スロット&sp=CAESAhAC',
    f'https://www.youtube.com/results?search_query=パチスロ&sp=CAESAhAC',
    f'https://www.youtube.com/results?search_query=パチプロ&sp=CAESAhAC',
    f'https://www.youtube.com/results?search_query=パチンカス&sp=CAESAhAC',
    f'https://www.youtube.com/results?search_query=パチンコ女子&sp=CAESAhAC',
    f'https://www.youtube.com/results?search_query=パチンコ実践&sp=CAESAhAC',
]

base_url = 'https://www.youtube.com'


for i in search_url:
    s.driver.get(i)
    time.sleep(20)

    for x in range(1, 81000):
        s.driver.execute_script("window.scrollTo(0, "+str(x)+");")
        s.driver.execute_script("return window.innerHeight")
        print(x)
    
    time.sleep(5)
    html = s.driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    labels = ['url', 'name', 'vido']
    dct_arr = []
    
    for z in soup.select("#main-link"):
        url = z.get('href')
        key = z.select_one('#text').text
        video = z.select_one('#video-count').text
        urls = {'url':f'{base_url}{url}', 'key':key, 'video':video }

        manga = collection1.find_one({'key': key})

        if not manga :
            collection2.insert_one(urls)
            print(urls)
            print('-'*40)
            
        else:
            print('被った')
            print('-'*40)


s.driver.quit()

        