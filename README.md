# Pixiv

![](https://img.shields.io/badge/python-3.9.3-green) ![](https://img.shields.io/badge/latest%20update-2022%2F10%2F5-green)



# 簡易說明

## 爬取方式

- pixiv排行榜

- pixiv作者圖庫

- 關鍵字作品

## 結構

`main.py`: 主程式

`./pixiv_catcher`： Pixiv爬蟲

`./template`: 爬取的資料範例

## 配置文件
- `config.ini`
  - `cookie` :Pixiv的cookies
  - `task_times`:每次會爬取多少張圖片，建議最多就150
  - `check_times`:爬取關鍵字作品所使用的比較收藏數，由於比較關鍵字的JSON資料網址爬蟲比較嚴格，建議最多就爬20
  - `cool_down`:每個任務啟動前的冷卻時間
- `config.json` : 剔除包含到不喜歡的關鍵字及作者
  - `badTag`: 黑名單關鍵字
  - `badUser`: 黑名單作者

## 設計微特點

- 採用asyncio 可以爬更快

- 採用`tqdm`爬取時會也跑取條


## 使用方式

- `python >=3.9`
- `pip install requirements.txt -r `
- 依需求修改配置文件
- 執行`main.py`
  - 輸入`a` 使用爬取作者
    - 輸入`作者的id`
    - 確認是否要設定`起始爬取id`(可以只爬取較新的作品)
  - 輸入`r` 使用爬取排行榜
    - 輸入要爬取的`排行榜日期`
    - 確認是要`綜合排行榜`or `GIF`
    - 確認是否是`週榜`
  - 輸入`t` 使用爬取作者
    - 輸入要爬取的`關鍵字`
    - 輸入爬取關鍵字作品的`起始日期`
    - 輸入關鍵字作品必須`大於多少收藏數`
