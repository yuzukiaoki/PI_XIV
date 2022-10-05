from pprint import pprint
import json,requests,os,zipfile,asyncio
import imageio.v2 as imageio
from aiohttp import ClientSession
async def main():

    
    illust_id = '99731123'



    cookie = ''
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
            'referer':f'https://www.pixiv.net/artworks/{illust_id}',
            'cookie':cookie}
            # 'referer':f'https://www.pixiv.net/artworks/{illust_id}'
    url =f"https://www.pixiv.net/ajax/illust/{illust_id}/ugoira_meta"
    real_url= 'https://i.pximg.net/img-zip-ugoira/img/2022/07/15/00/26/50/99727883_ugoira1920x1080.zip'
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            resp = await resp.json()
            pprint(resp)
    # response = requests.get(url,headers=headers).json()

        delay = [item["delay"] for item in resp["body"]["frames"]]
        print(delay)
        delay = sum(delay) / len(delay)
        zip_url = resp["body"]["originalSrc"]
        async with session.get(zip_url, headers=headers) as resp2:
            #gif_data = requests.get(zip_url, headers=headers)
            gif_data = await resp2.read()
            print(gif_data) 

    # # 資料夾建立
    # file_path = "bang"
    # if not os.path.exists(file_path):
    #     os.mkdir(file_path) 
    # zip_path = os.path.join(file_path, "temp.zip")
    # # wb+ 可以寫入和讀取
    # with open(zip_path, "wb+") as fp:
    #     fp.write(gif_data)
    # temp_file_list = []
    # # r -> read
    # zipo = zipfile.ZipFile(zip_path, "r")
    # # namlist 返回按名稱排序的檔案名稱列表
    # for file in zipo.namelist():
    #     temp_file_list.append(os.path.join(file_path, file))
    #     # extract 將檔案拆解出來
    #     zipo.extract(file, file_path)
    # # 沒關掉的話就不會寫入
    # zipo.close()

    # image_data = []
    # for file in temp_file_list:
    #     image_data.append(imageio.imread(file))
    #     imageio.mimsave(os.path.join(file_path, "UID_HERE" + ".gif"), image_data, "GIF", duration=delay / 1000)
    # # 清除所有中間文件。
    # print(temp_file_list)
    # for file in temp_file_list:
    #     os.remove(file)
    # os.remove(zip_path)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())