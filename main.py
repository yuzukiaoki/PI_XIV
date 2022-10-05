from pixiv_catcher import ranking, author, pixiv_tag_main
import time
import asyncio

rank = ranking.Pixiv_rank()
tag = pixiv_tag_main.Pixiv_Tag()
Author = author.Pixiv()

if __name__ == "__main__":


    # 確認執行花費的時間
    start_time = time.time()
    # 使用windows執行asyncio會有錯誤，必須多加下面這行
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    scrape_type = input("請輸入爬取想項目(author/rank/tag)\n").upper()
    if scrape_type =='A':
        print("===選用的是「author」===")
        asyncio.run(Author.main())
    
    elif scrape_type =='R':
        print("===選用的是「rank」===")
        asyncio.run(rank.main())
    
    elif scrape_type =='T':
        print("===選用的是「tag」===")
        asyncio.run(tag.main())

    else:
        print("輸入有誤請重新輸入")

    end_time = time.time()
    #取小數點後兩位
    use_time = round(end_time-start_time,2) 
    print(f"總共花費{use_time}秒")