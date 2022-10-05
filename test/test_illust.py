from pprint import pprint
import json,requests,os,zipfile,configparser
#99770216,99776830
# https://www.pixiv.net/artworks/99692202
illust_id = '100536261'
# 這個url能抓到作品資訊
url = f'https://www.pixiv.net/ajax/illust/{illust_id}?lang=zh-tw'
#
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
cookie = config['config']['cookie']
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
           'referer':f'https://www.pixiv.net/artworks/{illust_id}',
           'cookie':cookie}
           # 'referer':f'https://www.pixiv.net/artworks/{illust_id}'
#url ="https://www.pixiv.net/ajax/illust/99727883/ugoira_meta"
# response = requests.get(url,headers=headers) 這樣結果是 response[200]
response = requests.get(url,headers=headers).json()
#res_json = json.loads(response)
fileName = "illust.json"
# 寫入範例檔案 \template
# with open(fileName, "w",encoding='utf-8') as f:
#     json.dump(response, f, indent=4,ensure_ascii=False)
# 測試辨認json tag

# with open('config.json','r',encoding='utf8') as jfile:
#     jdata = json.load(jfile)
# tag_list = response['body']['tags']['tags']
# #pprint(tag_list[0]['tag'])
# for tag_num in tag_list:
#     if tag_num['tag'] in jdata['badTag']:
        
#         print("got u")
#     else:
#         print("not u")
# if response['body']['userId'] in jdata['badUser']:
#     print("fk u")
pprint(response['body'])



#body = response['body'] #可以看作者 作品的資訊
# body = res_json['body']['urls'] #作品的 所有url 
# pprint(body)

# body = res_json['body']['userName'].replace('\u3000','') 
# pprint(body)

# for datas in body:
#     download_url = datas['urls']['original']
#     print(download_url)
#     name = download_url.split('/')[-1]
#     content = requests.get(download_url,headers=headers).content
#     with open('pixiv-pictures'+'\\'+name,mode='wb')as f:
#         f.write(content)