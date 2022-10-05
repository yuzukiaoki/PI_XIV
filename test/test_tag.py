from pprint import pprint
import json,requests,os,zipfile,configparser

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini',encoding="utf-8")
cookie = config['config']['cookie']
illust_id = '99942371'
# 這個url能抓到作品資訊
# url = f'https://www.pixiv.net/ajax/illust/{illust_id}?lang=zh-tw'
tag = 'PUIPUIモルカー'
page =1
# url = f'https://www.pixiv.net/ajax/search/illustrations/{tag}%20{tag2}?word={tag}%20{tag2}&scd=2021-01-20&ecd=2022-06-20&mode=all&p={page}&s_mode=s_tag_full&type=all&lang=zh_tw'
url = f'https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&scd=2011-04-20&ecd=2022-07-30&mode=safe&p={page}&s_mode=s_tag_full&type=all&lang=zh_tw'
# 下面是沒有日期的
# f'https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&mode=all&p={page}&s_mode=s_tag_full&type=all&lang=zh_tw'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
           'referer':f'https://www.pixiv.net/',
           'cookie':cookie}
response = requests.get(url,headers=headers).json()

pprint(response['body']['illust']['total'])
# pprint(response['body']['illust']['data'][0]['id'])
# pprint(len(response['body']['illust']['data']))
#pprint(response)
fileName = "tag.json"
with open(fileName, "w",encoding='utf-8') as f:
    json.dump(response, f, indent=4,ensure_ascii=False)