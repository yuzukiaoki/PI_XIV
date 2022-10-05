from pprint import pprint
import json,requests,os
from aiohttp import ClientSession
import asyncio,configparser

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
cookie = config['config']['cookie']
id = '16274829'# 22976735 #25447095 #33955881
# 代理,根据自己实际情况调整,
# proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:51837'}
# proxy = 'http://your_user:your_password@your_proxy_url:your_proxy_port'
# proxy = "{'HTTP':'192.168.1.1:3128'}"
# os.environ["http_proxy"] = "http://127.0.0.1:7890"#要开代理，将7890换成你开梯子的端口
# os.environ["https_proxy"] = "http://127.0.0.1:7890"
#cookie = 'first_visit_datetime_pc=2022-07-13+12%3A19%3A40; p_ab_id=6; p_ab_id_2=0; p_ab_d_id=1971618170; yuid_b=EBcnkkQ; __utmc=235335808; device_token=b3ddce4bccede19fa529ca7e64534679; privacy_policy_notification=0; a_type=0; b_type=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; login_ever=yes; _gcl_au=1.1.1105521065.1657870450; _gid=GA1.2.180394193.1658105849; __utmz=235335808.1658132559.15.4.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/; __cf_bm=5n0_MHVbCV0M123XPig_hAceywgK9lVre.hbRxYxpCk-1658192080-0-AZTmDqMGy7jYRHJ+23zqbzfmQ2yFWLqOiwC8M7ElFdoHPOEfE+/fN7E6mzOWD5JcHCuO1N/CbZGg2tDrEQ6JZqMRp0tjFY3wDtyUEM7cPns+EpwVYgSLkd9BFqrawfn6BfoOEfpjsXF1LOyUe5TOs5Idk5/j1DO5TlyA7irt7QkABtiLxBweiaEr9EoowIGLbg==; __utma=235335808.1946082390.1657682419.1658132559.1658192122.16; __utmt=1; PHPSESSID=83982159_XQp0oMvszLTOqLJDVIZ1MEVsJITPln0Q; privacy_policy_agreement=4; c_type=23; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=83982159=1^9=p_ab_id=6=1^10=p_ab_id_2=0=1^11=lang=zh_tw=1; tag_view_ranking=Zy0Xn654Ig~KDro6UI7YG~jnIylc1mc7~562khdE7He~RTJMXD26Ak~0mJvQS2nSO~wvSOHClJ4f~1LN8nwTqf_~8irGFJpxES~Hpsa4d9POd~mz-N-j-QQQ~mFA0V1nbkC~fgp2llLuiV~OT4SuGenFI~ZXFMxANDG_~q3eUobDMJW~ziiAzr_h04~TqiZfKmSCg~_EOd7bsGyl~99-dVV-h9A~U-RInt8VSZ~t4OysW7qgq~YlBr401XTa~kBPO1025rT~Aa32YLGoo8~4zvmaEFfPQ~r1DegB7KWY~SY1hWzTBSP~rsKgvIMw_U~ZBoVMjk2oM~nZN-4cubzh~HLWLeyYOUF~dve3nXgd1M~dUhrZMpRPB~TPaY433as8~sr5scJlaNv~dvq-uhinPu~VN7cgWyMmg~2bq8SNVWly~F5CBR92p_Q~OfvEJkxqVs~EZQqoW9r8g~2R7RYffVfj~Lt-oEicbBr~U3xsMYG34O~zyKU3Q5L4C~GQbARAImfn~Gtd5A8fdBE~3SCfz3nhMC~Ie2c51_4Sp~sNpxKlBF43~Re1CX4f2XT~In4zmlN-R3~dyBU1gNHrS~T-I3moVoch~cTqZxDtC5Q~HOCPVxld3o~WLFQux9SLy~8Ul35U2eV8~WrF6omSikQ~hzJ6IAF8DJ~PD6gGce0rH~0KixsJBDVn~QzHaAvrA-w~on24wzx7AW~AU5OlIQ9Fy~mu7939gcfy~85s1qqXlWy~0Sds1vVNKR~wEwLYA3AVO; __utmb=235335808.10.10.1658192122; _ga=GA1.1.1946082390.1657682419; _ga_75BBYNYN9J=GS1.1.1658192106.18.1.1658192688.0'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
           'referer':f"https://www.pixiv.net/users/{id}/artworks" ,
           'cookie':cookie}
url2= f"https://pixiv.net/ajax/user/{id}/profile/top?lang=zh-tw" 
bang = f"https://pixiv.net/ajax/user/{id}/profile/all?lang=zh-tw"
async def main():
    async with ClientSession() as session:
        async with session.get(bang,headers=headers) as response:
            to_json = await response.json()
            #to_json = to_json["body"]["pickup"]
            #pprint(len(list(to_json["body"]["illusts"].keys())))
            #pprint(to_json)
            #print(bool(to_json))
            fileName = "author.json"
            with open(fileName, "w",encoding='utf-8') as f:
                json.dump(to_json, f, indent=4,ensure_ascii=False)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
