from pprint import pprint
import os,time
from aiohttp import ClientSession
from datetime import datetime as dt
import asyncio,zipfile,aiohttp,requests
import imageio.v2 as imageio
from itertools import islice, takewhile, repeat
from fake_useragent import UserAgent

#68943265,Seseren 16274829,26546165,30972875,4523203
ua = UserAgent()
user_agent = ua.random

def getAuthorName(to_json):
    """
    取得作者名稱
    :param to_json: json格式的資料
    """
    check_json = to_json["body"]["pickup"]
    # 如果pickup有資料，就取得作者名稱
    if check_json:
        # 如果作者名稱裡有 \u3000 則把它換成空白
        author_name = to_json["body"]["pickup"][0]["userName"].replace('\u3000','')
        return author_name
    else:
        # 如果pickup沒有資料，就用當下的日期取代作者名稱
        utc_time = dt.utcnow()
        author_name = utc_time.strftime('%Y%m%d')
        return author_name

def checkfolder(response,author_id):
    """
    :param response: 給予response至 getAuthorName()後得到作者名稱
    :param author_id: 作者id
    """
    folder_name = getAuthorName(response)
    first_path = os.getcwd()+'\\pixiv-artworks'
    if not os.path.exists(first_path):
        os.mkdir(first_path)

    path = os.getcwd()+'\\pixiv-artworks\\'+f"{folder_name}({author_id})"
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            raise Exception("無法建立資料夾")

    return path

def split_every(n, iterable):
    """
    Slice an iterable into chunks of n elements
    :type n: int
    :type iterable: Iterable
    :rtype: Iterator
    """
    iterator = iter(iterable)
    #time.sleep(1)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))

def request_gif(ugoira_id,path):

    cookie = ''
    headers = {'user-agent':user_agent,
            'referer':f'https://www.pixiv.net/artworks/{ugoira_id}',
            'cookie':cookie}
            
    url =f"https://www.pixiv.net/ajax/illust/{ugoira_id}/ugoira_meta"
    
    check_path = os.path.join(path, f"{ugoira_id}.gif")
    #print(check_path)
    if os.path.isfile(check_path):
        print(f"{ugoira_id} 已經存在")
        return False

    try:
        resp = requests.get(url,headers=headers).json()
        delay = [item["delay"] for item in resp["body"]["frames"]]
        # print(delay)
        delay = sum(delay) / len(delay)
        zip_url = resp["body"]["originalSrc"]
    except Exception as e:
        print(e)
        print(f"{ugoira_id} is not found")
        return False
        
    

    try:
        gif_data = requests.get(zip_url, headers=headers)
        gif_data = gif_data.content
    except Exception as e:
        print(e)
        print(f"{zip_url} 下載失敗")
        return False

    # 檔案路徑
    orignal_path = path
    path = os.path.join(path, f"{ugoira_id}")
    if not os.path.exists(path):
        os.mkdir(path)

    zip_path = os.path.join(path, "temp.zip")
    
    # wb+ 可以寫入和讀取
    with open(zip_path, "wb+") as fp:
        fp.write(gif_data)
    temp_file_list = []
    
    # r -> read
    zipo = zipfile.ZipFile(zip_path, "r")
    
    # namlist 返回按名稱排序的檔案名稱列表
    for file in zipo.namelist():
        temp_file_list.append(os.path.join(path, file))
        # extract 將檔案拆解出來
        zipo.extract(file, path)
    # 沒關掉的話就不會寫入
    zipo.close()

    
    image_data = []
    print(f"=====正在組成{ugoira_id}.gif=====")
    for file in temp_file_list:
        image_data.append(imageio.imread(file))
        imageio.mimsave(os.path.join(orignal_path, f"{ugoira_id}" + ".gif"), image_data, "GIF", duration=delay / 1000)
    
    # 清除所有中間文件。
    # print(temp_file_list)
    for file in temp_file_list:
        os.remove(file)
    os.remove(zip_path)
    # 刪除站存資料夾
    os.rmdir(path)
    
    print(f"{ugoira_id}, 下載完成")
    return True

async def dowload_GIF(ugoira_id,session,path,url):

    
    cookie = ''
    headers = {'user-agent':user_agent,
            'referer':f'https://www.pixiv.net/artworks/{ugoira_id}',
            'cookie':cookie}
            
    #url =f"https://www.pixiv.net/ajax/illust/{ugoira_id}/ugoira_meta"
    
    # utc_time = dt.utcnow()
    # time = utc_time.strftime('%H%M%S')
    try:
        async with session.get(url, headers=headers) as resp:
            resp = await resp.json()
            delay = [item["delay"] for item in resp["body"]["frames"]]
            # print(delay)
            delay = sum(delay) / len(delay)
            zip_url = resp["body"]["originalSrc"]
    except Exception as e:
        print(e)
        print(f"{ugoira_id} is not found")
        return False
        
    
    await asyncio.sleep(5)
    try:
        async with session.get(zip_url, headers=headers) as zip_resp:
            gif_data = await zip_resp.read()
    except Exception as e:
        print(e)
        print(f"{zip_url} 下載失敗")
        return False

    # 檔案路徑
    orignal_path = path
    path = os.path.join(path, f"{ugoira_id}")
    if not os.path.exists(path):
        os.mkdir(path)

    zip_path = os.path.join(path, "temp.zip")
    
    # wb+ 可以寫入和讀取
    with open(zip_path, "wb+") as fp:
        fp.write(gif_data)
    temp_file_list = []
    
    # r -> read
    zipo = zipfile.ZipFile(zip_path, "r")
    
    # namlist 返回按名稱排序的檔案名稱列表
    for file in zipo.namelist():
        temp_file_list.append(os.path.join(path, file))
        # extract 將檔案拆解出來
        zipo.extract(file, path)
    # 沒關掉的話就不會寫入
    zipo.close()

    
    image_data = []
    print(f"=====正在組成{ugoira_id}.gif=====")
    for file in temp_file_list:
        image_data.append(imageio.imread(file))
        imageio.mimsave(os.path.join(orignal_path, f"{ugoira_id}" + ".gif"), image_data, "GIF", duration=delay / 1000)
    
    # 清除所有中間文件。
    # print(temp_file_list)
    for file in temp_file_list:
        os.remove(file)
    os.remove(zip_path)
    # 刪除站存資料夾
    os.rmdir(path)
    #success = True
    print(f"{ugoira_id}, 下載完成")
    return True

async def fetch(session, url,headers,path):
    """
    :param session: 登入後的session
    :param url: 作品的URL
    :param headers: 登入後的cookie
    :param path: 資料夾路徑
    """
    async with session.get(url,headers=headers) as response:
        false_time = 0
        success_time = 0
        ugoira_id = []
        if response.status == 200:
            result_json =  await response.json()
            body = result_json['body']
            # 下載該作品 original的圖片
            for datas in body:
                download_url = datas['urls']['original']
                print(download_url)
                name = download_url.split('/')[-1]
                #如果有GIF則使用另外方式下載 # 爬取作品遇到gif的話就把ID放進list
                get_id = name.split('_')[0]
                check_path_jpg = os.path.join(path, f"{get_id}.jpg")
                check_path_png = os.path.join(path, f"{get_id}.png")
                if "ugoira" in name:
                    ugoira_id.append(get_id)

                    #await dowload_GIF(ugoira_id,session,path)
                elif os.path.isfile(check_path_jpg):
                    print(f"{get_id}.jpg 已經存在")
                    return 

                elif os.path.isfile(check_path_png):
                    print(f"{get_id}.png 已經存在")
                    return 
                          
                else:
                    #pass
                    async with session.get(download_url,headers=headers) as response:
                        result = response

                        if result.status == 200:
                            # 取得content的內容，不知道為什麼是用read() 隨便試出來的
                            content = await result.read()
                            # 寫入檔案
                            with open(path+'\\'+name,mode='wb')as f:
                                f.write(content)
                            success_time += 1
                        else:
                            print('下載失敗')
                            false_time += 1
        else:
            print("沒有找到作品，或是連線失敗")
        return success_time,false_time,ugoira_id

async def fetch_gif(session, id,headers,path):
    """
    :param session: 登入後的session
    :param url: 作品的URL
    :param headers: 登入後的cookie
    :param path: 資料夾路徑
    """
    url =f"https://www.pixiv.net/ajax/illust/{id}/ugoira_meta"
    async with session.get(url,headers=headers) as response:
        
        #目前認定作品GIF只會有一張，如果有多張的話要再探討
        #作品可能是 一張圖片或是多張圖片、多張圖片加一張GIF
        if response.status == 200:
            check_path = os.path.join(path, f"{id}.gif")
            #print(check_path)
            if os.path.isfile(check_path):
                print(f"{id} 已經存在")
                return False
            else:

                result =  await dowload_GIF(id,session,path,url)
                return result
            
            # result_json =  await response.json()
            # body = result_json['body']
            # # 下載該作品 original的圖片
            # for datas in body:
            #     download_url = datas['urls']['original']
            #     print(download_url)
            #     name = download_url.split('/')[-1]

                
            #     async with session.get(download_url,headers=headers) as response:
            #         result = response

            #         if result.status == 200:
            #             # 取得content的內容，不知道為什麼是用read() 隨便試出來的
            #             content = await result.read()
            #             # 寫入檔案
            #             with open(path+'\\'+name,mode='wb')as f:
            #                 f.write(content)
            #             success_time += 1
            #         else:
            #             print('下載失敗')
            #             false_time += 1
            
        else:
            print("沒有找到作品，或是連線失敗")
            
async def download(art,cookie,path):
    """
    :param art: 作者的作品list
    :param cookie: 登入後的cookie
    :param path: 資料夾路徑
    """
    
    links = []

    # art = hehe
    # 讀取list中所有ID
    # ua = UserAgent()
    # user_agent = ua.random
    for art_id in art:
        
        headers = {'user-agent':user_agent,
        'referer':f'https://www.pixiv.net/artworks/{art_id}',
        'cookie':cookie}
        
        art_url = f'https://www.pixiv.net/ajax/illust/{art_id}/pages?lang=zh'
        # 迴圈把所有作品的URL放進list
        links.append(art_url)
    
    print(f"總共有 {len(links)} 個作品")
    print("=====開始下載作品=====")
    await asyncio.sleep(3)

    timeout = aiohttp.ClientTimeout(total=600)
    connector = aiohttp.TCPConnector(limit=50,force_close=True)
    async with ClientSession(connector=connector,trust_env = True) as session:
        # 建立任務清單
        tasks = [fetch(session, link,headers,path) for link in links]
        # 打包任務清單及執行、下載一般非GIF圖片
        result = await asyncio.gather(*tasks)
        
        gif_id =[]
        
        for _,_,id in result:
            gif_id.extend(id)
        
        # await asyncio.sleep(10)
        success_list = []

        print(f"總共有 {len(gif_id)} 張GIF")
        print("=====開始下載GIF檔案=====")

        if len(gif_id) > 10:
            print("=====GIF數量大於10，使用request=====")
            await asyncio.sleep(3)
            for id in gif_id:
                res = request_gif(id,path)
                success_list.append(res)
        # 下載GIF圖片，且每次下載最多10個
        else:
            print("=====GIF數量小於10，使用aiohttp=====")
            gif_tasks = [fetch_gif(session, id,headers,path) for id in gif_id]
            for tasks in split_every(2, gif_tasks):
                # 獲取執行任務後的結果
                #await asyncio.sleep(1)
                success =  await asyncio.gather(*gif_tasks)
                success_list.append(success)
            

        # 回傳是為了讓主程式知道總共下載成功、失敗幾張圖片
        return result,success_list
        

async def main():

    author_id = input("請輸入作者ID:")
    # ua = UserAgent()
    # user_agent = ua.random
    cookie = ''
    headers = {'user-agent':user_agent,
           'referer':f"https://www.pixiv.net/users/{author_id}/artworks" ,
           'cookie':cookie}
    # 利用作者ID 找到作者所有作品ID
    author_url = f"https://pixiv.net/ajax/user/{author_id}/profile/all?lang=zh-tw"
    timeout = aiohttp.ClientTimeout(total=600)
    connector = aiohttp.TCPConnector(limit=50, force_close=True)
    async with ClientSession(connector=connector, trust_env = True) as session:
        async with session.get(author_url,headers=headers) as response:
            
            # 確認連線問題
            if response.status == 200:
                
                to_json = await response.json()
                #下載到目標位置
                dest = checkfolder(to_json,author_id)
                #作者 所有作品ID list
                art = list(to_json["body"]["illusts"].keys())
                
                # 如果有漫畫的作品
                if to_json["body"]["manga"]:
                    manga = list(to_json["body"]["manga"].keys())
                    # 合併(目前先合併，如非漫畫真的太多在另開資料夾存取)
                    art = art + manga
                result,gif_result =  await download(art,cookie,dest)
                success_time = 0
                false_time = 0
                # 從執行緒的list中 抓出每個執行緒的成功與失敗次數
                for times in result:
                    success_time += times[0]
                    false_time += times[1]

                print(f"成功下載IMG {success_time}張, 失敗{false_time}張")

                GIF_success = 0
                GIF_false = 0
                for result in gif_result:
                    if result == True:
                        GIF_success += 1
                    elif result == False:
                        GIF_false += 1
                print(f"成功下載GIF {GIF_success}張, 失敗{GIF_false}張")


            else:
                raise Exception("此作者不存在，或是連線有問題")


if __name__ == "__main__":
    # 確認執行花費的時間
    start_time = time.time()
    
    # 使用windows執行asyncio會有錯誤，必須多加下面這行
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    end_time = time.time()
    #取小數點後兩位
    use_time = round(end_time-start_time,2) 
    print(f"總共花費{use_time}秒")