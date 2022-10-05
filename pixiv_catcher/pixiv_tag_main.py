
from pprint import pprint
import os,time
from aiohttp import ClientSession
from datetime import datetime as dt
import asyncio,aiohttp

from tqdm import tqdm
from utility import get_artwork,headersss,download_result

#68943265,Seseren 16274829,26546165,30972875,4523203,7120604
class Pixiv_Tag():

    def __init__(self):
        
        pass

    def checkfolder(self,tag):
        """
        :param response: 給予response至 getAuthorName()後得到作者名稱
        :param author_id: 作者id
        """
        #folder_name = self.getAuthorName(response)
        first_path = os.getcwd()+'\\pixiv-tag'
        if not os.path.exists(first_path):
            os.mkdir(first_path)

        self.path = os.getcwd()+'\\pixiv-tag\\'+f"{tag}"
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except:
                raise Exception("無法建立資料夾")


    async def main(self):
        
        now_date = dt.now()
        now_date = now_date.strftime('%Y-%m-%d')
        tag = input("請輸入欲下載的標籤：\n")
           
        while True:
            try:
                start_date = input("請輸入起始日期(ex:20190101):\n")
                #檢查日期格式，沒問題後轉換日期格式(20190101->2019-01-01)
                start_date = dt.strptime(start_date, '%Y%m%d')
                start_date = start_date.strftime('%Y-%m-%d')
                break
            except ValueError:
                print("請輸入正確的日期格式")
        #結束日期固定選當下日期
        #end_date = input("請輸入結束日期(ex:2019-01-01):")
        while True:
            #檢查收藏數是否為整數
            # 輸入完收藏數後 可能遇到 status 403 也許可以重複嘗試幾次
            self.favorites = input("請輸入收藏數(ex:100):\n")
            if self.favorites.isdigit() == False:
                print("請輸入數字")
                continue
            break
        page = 1

        #確認這個標籤總共有多少作品
        tag_url = f'https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&scd={start_date}&ecd={now_date}&mode=safe&p={page}&s_mode=s_tag&type=all&lang=zh_tw'
        #s_mode = s_tag =>部分一致
        #s_mode = s_tag_full => 完全一致
        referer = f"https://www.pixiv.net/tags/{tag}/artworks?mode=safe&scd={start_date}&ecd={now_date}&s_mode=s_tag&lang=zh_tw&p={page}"
        timeout = aiohttp.ClientTimeout(total=600)
        connector = aiohttp.TCPConnector(force_close=True)
        async with ClientSession(connector=connector,trust_env = True,timeout=timeout) as session:
            async with session.get(tag_url,headers=headersss(referer)) as response:
                
                try_count = 0
                while True:
                    try:
                        to_json = await response.json()

                        total = to_json['body']['illust']['total']
                        if total == 0:
                            raise Exception("該標籤沒有任何作品，確認標籤是否正確")

                        print(f"標籤:{tag}總共有{total}個作品")
                        while True:
                            page_count = round(total/60)
                            if total%60 == 0:
                                print(f"要爬{page_count}頁才爬得完")
                            else:
                                print(f"要爬{page_count+1}頁才爬得完")
                            #檢查頁數是否為整數
                            page = input("請輸入要爬取的頁數(每頁有60個作品):\n")
                            if page.isdigit() == False:
                                print("請輸入數字")
                                continue
                            break    

                        self.checkfolder(tag)
                        art_list = []
                        with tqdm(total=len(range(1,int(page)+1)),desc="爬取作品") as pbar:
                        #根據page的頁數爬取作品
                            for page in range(1,int(page)+1):

                                referer = f"https://www.pixiv.net/tags/{tag}/artworks?mode=safe&scd={start_date}&ecd={now_date}&s_mode=s_tag&lang=zh_tw&p={page}"
                                tag_url = f'https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&scd={start_date}&ecd={now_date}&mode=safe&p={page}&s_mode=s_tag&type=all&lang=zh_tw'
                                async with session.get(tag_url,headers=headersss(referer)) as response:
                                    try:
                                    
                                        json_response = await response.json()
                                        pbar.update()
                                        if json_response['body']['illust']['data'] == []:
                                            # print(tag_url)
                                            # print("沒有更多作品了")

                                            break

                                        for i in range(0,len(json_response['body']['illust']['data'])):

                                            #把當頁的作品ID放進list
                                            art_list.append(json_response['body']['illust']['data'][i]['id'])
                                        
                                    except Exception as e:
                                        raise Exception(f"發生錯誤: {e}\n response.status: {response.status}")

                            
                        # result,gif_result =  await self.download(art_list,session)
                        result,gif_result =  await get_artwork(art_list, session, self.path, scrape_type ='tag', favorites=self.favorites)

                        success_time = 0
                        false_time = 0
                        # 從執行緒的list中 抓出每個執行緒的成功與失敗次數
                        success_time,false_time = download_result(tuple=result)

                        print(f"成功下載IMG {success_time}張, 失敗{false_time}張")

                        if gif_result != []:
                            GIF_success,GIF_false = download_result(list=gif_result)

                            print(f"成功下載GIF {GIF_success}張, 失敗{GIF_false}張")
                        # print("錯誤總數",self.error_count)
                        # print("總排除數",self.exclude_count)

                        break
                    except Exception as e:
                        try_count += 1
                        print(f"發生錯誤: {e}\n response.status: {response.status}")
                        print(f"目前錯誤次數 {try_count}次")
                        if try_count == 3:
                            print("錯誤次數已達 3 次")
                            raise Exception(f"發生錯誤: {e}\n response.status: {response.status}")

                        await asyncio.sleep(20*try_count)
                        #raise Exception(f"發生錯誤: {e}\n response.status: {response.status}")


if __name__ == "__main__":
    # 確認執行花費的時間
    start_time = time.time()
    
    # 使用windows執行asyncio會有錯誤，必須多加下面這行
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(Pixiv_Tag().main())

    end_time = time.time()
    #取小數點後兩位
    use_time = round(end_time-start_time,2) 
    print(f"總共花費{use_time}秒")
    