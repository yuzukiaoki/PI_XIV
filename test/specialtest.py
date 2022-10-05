import configparser
from textwrap import indent
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
# cookie = config['config']['cookie']
#config.add_section('bang')
config.set('config','heheqwewqee123','haha321')
with open ('config.ini', 'w+',encoding='utf-8') as configfile:
    config.write(configfile)

# from tqdm import tqdm
# import time
# loss=50
# with tqdm(total=50,desc="測試") as pbar:
#     for i in range(50):
#         time.sleep(0.5)
#         loss = loss - 1
#         pbar.update()
#         pbar.set_postfix({'lost':'{0:1.5f}'.format(loss)})
        # if i == 30:
        #     pbar.close()
        #     break
        # if i == 5:
        #      pbar.set_description("測試2")
        #      adict = {"測試":"測試"}
        #      pbar.set_postfix(adict)
        #      pbar.refresh()
        #      pbar.close()
#             pbar.update(50)
#             pbar.set_description("測試3")
#             pbar.set_postfix({"測試":"測試"})
#             pbar.refresh()
#             pbar.close()

# for i in tqdm(range(1, 60)):
#     """ 代碼 """
# # 假設這代碼部分需要0.05s，循環執行60次
#     time.sleep(0.05)