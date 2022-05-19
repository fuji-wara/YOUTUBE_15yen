from pymongo import MongoClient
from bs4 import BeautifulSoup
import se as s
import time
import datetime
from datetime import datetime as dt
import math
import statistics
import re


# mongo 設定
client = MongoClient('localhost', 27017) # ローカルホストDBに接続。
collection1 = client.YOUTUBE.channel_list2
collection2 = client.YOUTUBE.completion_list


def main():
    x = 0
    z = []
    for v in collection1.find():
        z.append(v)

    for i in z:
        x += 1
        print(x)
        channel_title = i['チャンネル名']
        channel_url = i['チャンネルURL']
        channel_all = i['動画本数']

        channel_dict = scrap_cannel(channel_title, channel_url, channel_all)
        try:
            collection2.insert_one(channel_dict)
            print(channel_dict)
        except:
            print(f'{channel_title} 失敗')
    
    s.driver.quit()


def scrap_cannel(channel_title, channel_url, channel_all):
    """
    受け取ったURLで総投稿数・投稿頻度・最新日を取得して辞書にする
    """
    base_url = 'https://www.youtube.com'
    all_videos = channel_all 

    # 投稿頻度・最新日を取得する。
    s.driver.get(f'{channel_url}/videos')
    time.sleep(5)
    html_2 = s.driver.page_source.encode('utf-8')
    soup_2 = BeautifulSoup(html_2, 'lxml')
    num = 0
    day_list = []
    for i in soup_2.select('ytd-grid-video-renderer.style-scope.ytd-grid-renderer'):
        if num >= 6:
            break

        x = i.select_one('a#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail').get('href') 
        z = f'{base_url}{x}'

        s.driver.get(z)
        time.sleep(10)
        html_3 = s.driver.page_source.encode('utf-8')
        soup_3 = BeautifulSoup(html_3, 'lxml')
        pattern = r'\b\d{4}/\d{2}/\d{2}\b'

        try:
            try: # 通常動画
                day = soup_3.find(id="info-strings" ).find("yt-formatted-string", class_="style-scope ytd-video-primary-info-renderer").text
                day = re.search(pattern, day).group()
                print(day)
                day_list.append(day)

            except: # ショート動画
                s.driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[1]/ytd-reel-video-renderer[1]/div[2]/ytd-reel-player-overlay-renderer/div[2]/div[1]/ytd-menu-renderer/yt-icon-button/button/yt-icon').click()
                time.sleep(2)
                s.driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-icon').click()
                time.sleep(5)
                element = s.driver.find_elements_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-reel-description-sheet-renderer/div[2]/div/yt-formatted-string/span[1]')
                time.sleep(2)
                day = element[0].text
                day = re.search(pattern, day).group()
                print(day)
                day_list.append(day)
        except:
            print('sippai')

        num += 1

    try:
        latest_day = day_list[0] # 最新投稿日
    except:
        latest_day = 0 
        print('latest_day 失敗')

    try:
        x = []
        a = len(day_list) # リストの要素数
        b = 0
        c = 1
        for d in range(1, a):
            e = day_list[b].replace('/', '')
            f = day_list[c].replace('/', '')

            g = datetime.datetime.strptime(e, '%Y%m%d')
            h = datetime.datetime.strptime(f, '%Y%m%d')
            i = g-h
            x.append(i.days)
            b += 1
            c += 1
        
        j = math.floor(statistics.mean(x))
        post_frequenc = f'{j}日に1回'

    except:
        post_frequenc = '1日に1回'

    channel_dict = {'チャンネル名': channel_title, 'チャンネルURL': channel_url, '投稿頻度': post_frequenc, '最新動画投稿日':latest_day, '動画本数': all_videos}

    return channel_dict


if __name__ == '__main__':
    main()


# mongoexport --host="localhost" --port=27017 --db="YOUTUBE" --collection="completion_list" --type="csv" --out="iofs1.csv" --fields="チャンネル名,チャンネルURL,投稿頻度,最新動画投稿日,動画本数" --noHeaderLine