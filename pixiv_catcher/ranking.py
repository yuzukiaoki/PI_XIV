from pprint import pprint
import os
from time import time
import aiohttp, json
from aiohttp import ClientSession
# import zipfile
from asyncio import run,set_event_loop_policy,WindowsSelectorEventLoopPolicy
#import datetime as dt
from datetime import timedelta
#import imageio.v2 as imageio
from datetime import datetime
from utility import get_artwork,download_result,headersss

class Pixiv_rank():

    def __init__(self):

        self.exclude =[]
        

    def date_math(self,str_date,minus_day):
        """
        :param str_date: 日期字串
        :param minus_day: 減去的天數
        :return: 日期字串
        """
        date_obj = datetime.strptime(str_date,'%Y%m%d')
        date_obj = date_obj - timedelta(days=minus_day)
        date_obj = date_obj.strftime('%Y%m%d')
        return date_obj

    def checkfolder(self,response):
        """
        :param response: 給予response至 getAuthorName()後得到作者名稱
        """

        first_path = os.getcwd()+'\\pixiv-ranking'
        if not os.path.exists(first_path):
            os.mkdir(first_path)

        date = response['date']
        # # 將str轉成datetime
        # date_obj = datetime.strptime(date,'%Y%m%d')
        # # 這週的排行榜
        # first_date = date_obj - timedelta(days=6)
        # # 轉回str
        first_date = self.date_math(response['date'],6)


        if self.folder_check == "normal_weekly":
            self.path = os.getcwd()+'\\pixiv-ranking\\'+f"pixiv_週榜({first_date}-{date})"
        
        elif self.folder_check == "normal_daily":
            self.path = os.getcwd()+'\\pixiv-ranking\\'+f"pixiv_日榜({date})"


        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except:
                raise Exception("無法建立資料夾")


    async def main(self):
        
        input_date = input("請輸入日期(EX:20220716):\n")


        input_M = input("是否綜合插圖(Y/N):\n").upper()
        # 否就是日榜
        input_type = input("是否週榜(Y/N):\n").upper()


        # 只有 日排行榜 和 週排行榜 和男性排行榜
        #色色最多到 第二頁
        total_success = 0
        total_success_gif = 0
        total_false = 0
        total_false_gif = 0

        for_range = 3
        # GIF榜只有一頁
        if input_M == "N" and input_type == "Y":
            for_range = 2
        elif input_M == "N" and input_type == "N":
            for_range = 2

        # range 只有不到50 很可能是有作品被刪除或是隱藏
        for page in range(1,for_range):

            if input_M == "Y" and input_type == "Y":
                # 一般周榜
                self.folder_check = "normal_weekly"
                url= f"https://www.pixiv.net/ranking.php?p={page}&mode=weekly&date={input_date}&format=json"

            elif input_M == "Y" and input_type == "N":
                # 一般日榜
                self.folder_check = "normal_daily"
                url= f"https://www.pixiv.net/ranking.php?p={page}&mode=daily&date={input_date}&format=json"
            
            else:
                raise Exception("輸入有誤，重來")

            downloadURL = []
            second = False
            # 檔名命名方式  名次_尾巴檔名
            # 需要的東西: url、rank
            with open('config.json','r',encoding='utf8') as jfile:
                jdata = json.load(jfile)

            timeout = aiohttp.ClientTimeout(total=600)
            connector = aiohttp.TCPConnector(limit=50, force_close=True)

            async with ClientSession(connector=connector, trust_env = True, timeout=timeout) as session:

                async with session.get(url,headers=headersss("https://www.pixiv.net/ranking.php"),max_redirects=30) as resp:
                   
                    to_json = await resp.json()
                    # 確認該排行榜是否存在(排行榜存在的話就不會有error這個key)
                    check = bool(to_json.get('error',False))
                    if check:
                        raise Exception('沒有找到排行榜，最新的排行榜只有今天日期-2')

                    # 確認連線問題
                    if resp.status == 200:

                        self.checkfolder(to_json)
                        resp = to_json['contents']
                        
                        for url in range(0,len(resp)):
                            for tag in resp[url]['tags']:
                                if tag in jdata['badTag']:
                                    self.exclude.append(resp[url]['illust_id'])
                                    continue
                            if resp[url]['user_id'] in jdata['badUser']:
                                self.exclude.append(resp[url]['illust_id'])
                                continue

                            downloadURL.append(resp[url]['illust_id'])

                        if page == 2:
                            second = True
                        result,gif_result = await get_artwork(downloadURL, session, self.path, scrape_type='rank', second=second)
                        
                        # 從執行緒的list中 抓出每個執行緒的成功與失敗次數
    
                        success_time,false_time = download_result(tuple=result)

                        print(f"成功下載IMG {success_time}張, 失敗{false_time}張")

                        total_success += success_time
                        total_false += false_time

                        if gif_result != []:
                            GIF_success,GIF_false = download_result(list=gif_result)

                            print(f"成功下載GIF {GIF_success}張, 失敗{GIF_false}張")

                            total_success_gif += GIF_success
                            total_false_gif += GIF_false

                    else:
                        print("此作者不存在，或是連線有問題")
                        raise Exception("連線狀態",resp.status)

        print("=====下載完成=====")
        print(f"排除的作品: {self.exclude}")

        print(f"總共成功下載IMG {total_success}張, 失敗{total_false}張")

        if gif_result != []:
            print(f"總共成功下載GIF {total_success_gif}張, 失敗{total_false_gif}張")
        

if __name__ == "__main__":
    # 確認執行花費的時間
    start_time = time()
    
    # 使用windows執行asyncio會有錯誤，必須多加下面這行
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run(Pixiv_rank().main())

    end_time = time()
    #取小數點後兩位
    use_time = round(end_time-start_time,2) 
    print(f"總共花費{use_time}秒")

# TooManyRedirects 很可能是cookies過期