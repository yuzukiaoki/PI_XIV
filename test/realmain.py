from pprint import pprint
import json,requests,os,time


def getAuthorName(to_json):
    """
    取得作者名稱
    :param to_json: response轉成json
    """
    # 如果作者名稱裡有 \u3000 則把它換成空白
    author_name = to_json["body"]["pickup"][0]["userName"].replace('\u3000','')
    
    return author_name


def checkfolder(response,author_id):
    """
    :param response: 給予response至 getAuthorName()後得到作者名稱
    :param author_id: 作者id
    """
    folder_name = getAuthorName(response)
    first_path = os.getcwd()+'\\pixiv'
    if not os.path.exists(first_path):
        os.mkdir(first_path)

    path = os.getcwd()+'\\pixiv\\'+f"{folder_name}({author_id})"
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            raise Exception("無法建立資料夾")

    return path

def downloadImg(art,cookie,path):
    """
    :param art: 作者的作品list
    :param cookie: 登入後的cookie
    :param path: 資料夾路徑
    """
    false_time = 0
    success_time = 0
    # 讀取list中所有ID
    for id in art:

        art_id = id
        
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
        'referer':f'https://www.pixiv.net/artworks/{art_id}',
        'cookie':cookie}
        # 此url 抓到作品url
        art_url = f'https://www.pixiv.net/ajax/illust/{art_id}/pages?lang=zh'
        response = requests.get(art_url,headers=headers)
        result_check = bool(response.status_code ==200)
        if result_check:
            # 抓到的json
            result_json = response.json()
            body = result_json['body']
            # 下載該作品 original的圖片
            for datas in body:
                download_url = datas['urls']['original']
                print(download_url)
                name = download_url.split('/')[-1]
                response = requests.get(download_url,headers=headers)
                content_check = bool(response.status_code == 200)
                if content_check:
                    # 取得content的內容
                    content = response.content
                    with open(path+'\\'+name,mode='wb')as f:
                        f.write(content)
                    success_time += 1
                else:
                    print('下載失敗')
                    false_time += 1
                    continue
        else:
            print("沒有找到作品，或是連線失敗")
            continue
    return false_time,success_time

def main():

    author_id = input("請輸入作者ID:")

    cookie = ''
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
           'referer':f"https://www.pixiv.net/users/{author_id}/artworks" ,
           'cookie':cookie}
    # 利用作者ID 找到作者所有作品ID
    author_url = f"https://pixiv.net/ajax/user/{author_id}/profile/all?lang=zh-tw"
    response = requests.get(author_url,headers=headers)
    to_json = response.json()
    result = bool(response.status_code ==200)

    # 確認連線問題
    if result:
        #下載到目標位置
        dest = checkfolder(to_json,author_id)
        #作者 所有作品ID list
        art = list(to_json["body"]["illusts"].keys())

        false_time,success_time =downloadImg(art,cookie,dest)
        
        print(f"成功{success_time}張, 失敗{false_time}張")

        

    else:
        raise Exception("此作者不存在，或是連線有問題")

    

if __name__ == "__main__":
    start_time = time.time()
    
    main()
    end_time = time.time()
    print(f"總共花費{end_time-start_time}秒")