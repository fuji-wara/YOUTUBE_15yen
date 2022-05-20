from pymongo import MongoClient
from bs4 import BeautifulSoup
import se as s
import time
import re

# mongo 設定
client = MongoClient('localhost', 27017) # ローカルホストDBに接続。
collection1 = client.YOUTUBE.new_channel2
collection2 = client.YOUTUBE.channel_list2

# 変数
two_months_ago = '2022/2/27'
base_url = 'https://www.youtube.com'


def main():
    x = 0
    z = []
    for c in collection1.find():
        z.append(c)
    for i in z:
        x += 1
        print(x)
        channel_title = i['key']
        channel_url = i['url']
        channel_all = i['video']
        channel_dict = scrap_cannel(channel_title, channel_url, channel_all)
        try:
            if any(channel_dict):
                collection2.insert_one(channel_dict)
                print(channel_dict)
            else:
                print('2ヶ月以上')
        except:
            print('動画なし')

    s.driver.quit()


def scrap_cannel(channel_title, channel_url, channel_all):
    """
    リサーチ済み、最新動画が二ヶ月前か確認して辞書作成。
    """
    all_vidos = re.sub(r"\D", "", channel_all) # 正規表現で数字のみ取得

    s.driver.get(f'{channel_url}/videos')
    time.sleep(5)
    html1 = s.driver.page_source.encode('utf-8')
    soup1 = BeautifulSoup(html1, 'lxml')
    num = 0
    for j in soup1.select('ytd-grid-video-renderer.style-scope.ytd-grid-renderer'):
        if num >= 1:
            break
        z = j.select_one('a#thumbnail.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail').get('href') 
        latest_day_url =f'{base_url}{z}'

        s.driver.get(latest_day_url)
        time.sleep(10)
        html2 = s.driver.page_source.encode('utf-8')
        soup2 = BeautifulSoup(html2, 'lxml')
        pattern = r'\b\d{4}/\d{2}/\d{2}\b'
        try:
            try: # 通常動画
                day = soup2.find(id="info-strings" ).find("yt-formatted-string", class_="style-scope ytd-video-primary-info-renderer").text
                day = re.search(pattern, day).group()

            except: # ショート動画
                s.driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[1]/ytd-reel-video-renderer[1]/div[2]/ytd-reel-player-overlay-renderer/div[2]/div[1]/ytd-menu-renderer/yt-icon-button/button/yt-icon').click()
                time.sleep(2)
                s.driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-icon').click()
                time.sleep(5)
                element = s.driver.find_elements_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-reel-description-sheet-renderer/div[2]/div/yt-formatted-string/span[1]')
                time.sleep(2)
                day = element[0].text
                day = re.search(pattern, day).group()
    
        except:
            print('sippai')
            latest_day  = ''
            channel_dict = {'チャンネル名': channel_title, 'チャンネルURL': channel_url, '投稿頻度':'', '最新動画投稿日':latest_day, '動画本数': all_vidos}
            return channel_dict

        latest_day = day
        num += 1

        first_data = latest_day
        second_data = two_months_ago

        format1 = time.strptime(first_data, "%Y/%m/%d")
        format2 = time.strptime(second_data, "%Y/%m/%d")

        if format1 > format2 :
            channel_dict = {'チャンネル名': channel_title, 'チャンネルURL': channel_url, '投稿頻度':'', '最新動画投稿日':latest_day, '動画本数': all_vidos}
            return channel_dict
        else:
            channel_dict = {}
            return channel_dict



if __name__ == '__main__':
    main()