import scrapy
import json
import os  # 导入os模块，用于读取海报文件夹
from douban_scrapy.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = []
    start_urls = []

    def start_requests(self):
        json_path = "../douban_top250.json"
        with open(json_path, "r", encoding="utf-8-sig") as f:
            movies = json.load(f)

        poster_dir = "../posters"
        poster_map = {}
        # 遍历所有海报文件
        if os.path.exists(poster_dir):
            for file in os.listdir(poster_dir):
                if file.endswith(".jpg"):
                    movie_title = file.replace(".jpg", "")
                    poster_map[movie_title] = f"posters/{file}"

        for movie in movies:
            item = MovieItem()
            item["rank"] = movie.get("rank")
            item["title"] = movie.get("title")
            item["title_en"] = movie.get("title_en", "")
            item["score"] = movie.get("score")
            item["vote_num"] = movie.get("vote_num")
            item["director"] = movie.get("director")
            item["actors"] = movie.get("actors")
            item["intro"] = movie.get("intro")
            item["year"] = movie.get("year")
            item["duration"] = movie.get("duration")
            item["genre"] = movie.get("genre")
            item["imdb"] = movie.get("imdb")
            item["url"] = movie.get("url")

            item["poster_url"] = poster_map.get(item["title"], "")

            if not item["rank"]:
                self.logger.warning(f"跳过空排名电影：{item['title']}")
                continue

            yield item