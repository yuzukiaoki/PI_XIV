import asyncio
import json
import time,configparser
from pprint import pprint

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup

# https://www.pixiv.net/artworks/99692202
illust_id = '100733714'
url = f'https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=zh'
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
cookie = config['config']['cookie']

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
           'referer':f'https://www.pixiv.net/artworks/{illust_id}',
           'cookie':cookie}
#url = 'https://httpbin.org/ip'
# # response = requests.get(url,headers=headers) 這樣結果是 response[200]
response = requests.get(url,headers=headers).json()
#res_json = json.loads(response)
#proxy = 'http://106.107.205.112:80'
fileName = "illust_dowload_url.json"
# with open(fileName, "w",encoding='utf-8') as f:
#     json.dump(response, f, indent=4,ensure_ascii=False)
pprint(response)

# body = response['body']
# start_time = time.time()
# for datas in body:
#     download_url = datas['urls']['original']
#     print(download_url)
#     name = download_url.split('/')[-1]
#     content = requests.get(download_url,headers=headers).content
#     #print(content)
#     with open('pixiv-pictures'+'\\'+name,mode='wb')as f:
#         f.write(content)
# end = time.time()
# print(end-start_time)

# async def main(illust_id):

#     urls = []
#     async with ClientSession() as session:
#         tasks = [fetch(session, url) for url in urls]

#         await asyncio.gather(*tasks)

# async def fetch():
#     async with ClientSession() as session:
#         async with session.get(url, headers= headers) as response:
#             #print(response.status)
#             json_content = await response.json()
#             #print(json_content)
#             body = json_content['body']
#             start = time.time()
#             for datas in body:
#                 download_url = datas['urls']['original']
#                 #print(download_url)
#                 name = download_url.split('/')[-1]
#                 async with session.get(download_url, headers= headers) as response: # 看起來是必加的
#                     print(response.status)
#                     content = await response.read()
#                     #print(content)
                    
#                     with open('pixiv-pictures'+'\\'+name,mode='wb')as f:
#                         f.write(content)
#                     break
#             end = time.time()
#             print(f'{end-start}')
#             #pprint(json_content)
#             #return await response.json()

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(fetch())
