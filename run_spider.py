from spider_requests import crawl_top250
from spider_selenium_edge import crawl_detail
from poster_downloader import download_poster
from db import create_tables, insert_movie, insert_comment
from tqdm import tqdm
import json
import csv


def main():
    print("正在创建数据库表...")
    create_tables()

    print("开始爬取豆瓣TOP250列表...")
    movies = crawl_top250()

    all_data = []
    print("开始爬取详情页与短评...")

    for m in tqdm(movies):
        detail = crawl_detail(m["url"])
        
        download_poster(m["title"], m.get("poster_url", ""))

        data = {
            "rank": m["rank"],
            "title": m["title"],
            "title_en": m["title_en"],
            "score": m["score"],
            "vote_num": m["vote_num"],
            "director": m["director"],
            "actors": m["actors"],
            "intro": m["intro"],
            "year": detail.get("year", ""),
            "genre": detail.get("genre", ""),
            "duration": detail.get("duration", ""),
            "imdb": detail.get("imdb", ""),
            "url": m["url"]
        }

        mid = insert_movie(data)

        for c in detail.get("comments", []):
            insert_comment(mid, c)

        all_data.append(data)

    # 导出JSON
    with open("douban_top250.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    # 导出CSV
    with open("douban_top250.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["排名", "片名", "评分", "评价人数", "导演", "主演", "简介", "年份", "类型", "片长", "IMDb", "链接"])
        for item in all_data:
            w.writerow([
                item["rank"],
                item["title"],
                item["score"],
                item["vote_num"],
                item["director"],
                item["actors"],
                item["intro"],
                item["year"],
                item["genre"],
                item["duration"],
                item["imdb"],
                item["url"]
            ])

    print("✅ 全部爬取完成！数据已保存到数据库、JSON、CSV")


if __name__ == "__main__":
    main()