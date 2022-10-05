
import json
import requests
from fake_useragent import UserAgent
from PIL import Image
from io import BytesIO
import os

ua = UserAgent()
headers = {
    'authority': 'www.pixiv.net',
    'sec-ch-ua': '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'accept': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'user-agent': ua.random,
    'x-user-id': '你的id',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.pixiv.net/',
    'accept-language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': '你的cookie',
}
paramsPage = (
    ('lang', 'zh_tw'),
)

def artWorkShow(artWorkUrl, headers):
    response = requests.get(artWorkUrl, headers=headers)
    image = Image.open(BytesIO(response.content))
    image.show()

def getTagAllPicId(url, headers, params):
    listIllusts = []
    response = requests.get(url, headers = headers, params = params)
    if response.status_code == 200:
        for i in range(0, 60):
            resdict = json.loads(response.content)['body']['illust']['data'][i]['id']
            listIllusts.append(resdict)
        return listIllusts

def getArtWorkPage(url, headers, params, setBookmark):
    response = requests.get(url, headers = headers, params = params)
    if response.status_code == 200:
        resdict = json.loads(response.content)

        artWorkBookmark = resdict['body']['bookmarkCount']
        print(artWorkBookmark)

        if artWorkBookmark >= setBookmark:
            artWorkUrl = resdict['body']['urls']['original']
            artWorkTitle = resdict['body']['title']
            artWorkId = resdict['body']['id']
            print("--------------------------------------------------")
            print(artWorkUrl)
            print(artWorkTitle)
            print(artWorkId)
            print("--------------------------------------------------")
            #artWorkShow(artWorkUrl, headers)   #這裡可以選擇要不要把每個爬取到的圖片打開
            artWorkDownLoad(artWorkUrl, artWorkTitle, artWorkId, headers)
                

def artWorkDownLoad(artWorkUrl, artWorkTitle, artWorkId, headers):
    os.makedirs(f"C://Users//Desktop//雜物//Pixiv//{tag}", exist_ok=True)    #沒有這個標籤資料夾時創建一個 #處存位置
    downLoadTitle = f"{artWorkTitle}-{artWorkId}"
    filePath = f"/Users/Desktop/雜物/Pixiv/{tag}" + "/{}.png".format(downLoadTitle)   #存圖片的位置
    with open(filePath, "wb+") as file:
        imgData = requests.get(artWorkUrl.format(artWorkTitle), headers=headers).content
        try:
            file.write(imgData)
            print("成功下載圖片: {}".format(downLoadTitle))
        except Exception:
            print("未成功下載圖片: {}".format(downLoadTitle))

#tag = "綾波レイ"
#setBookmark = 1000
#setPage = 10

tag = str(input("請輸入標籤: "))
setBookmark = int(input("請輸入收藏數: "))
openPage = int(input("從第幾頁開始: "))
setPage = int(input("要爬取幾頁: ")) + 1

for page in range(openPage, setPage):
    print(f"第{page}頁開始，總共{setPage - 1}頁")
    paramsTag = {                    #請求標頭
        'word' : tag,
        'order': 'date_d',
        'mode': 'all',
        'p': f'{page}',
        's_mode': 's_tag_full',
        'type': 'illust_and_ugoira',
        'lang': 'zh_tw',
        }
    urlTag = f'https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&order=date_d&mode=all&p={page}&s_mode=s_tag_full&type=illust_and_ugoira&lang=zh_tw'


    artWorkIllusts = getTagAllPicId(urlTag, headers, paramsTag)

    for i in range(0, 60):
        urlIllusts = f"https://www.pixiv.net/ajax/illust/{artWorkIllusts[i]}?lang=zh_tw"
        getArtWorkPage(urlIllusts, headers, paramsPage, setBookmark)
    print(f"第{page}頁結束，總共{setPage - 1}頁")