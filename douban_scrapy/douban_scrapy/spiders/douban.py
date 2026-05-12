import scrapy
import json
import os  # 导入os模块，用于读取海报文件夹
from douban_scrapy.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = []
    start_urls = []

    def start_requests(self):
        # 1. 读取成员A的电影JSON数据
        json_path = "../douban_top250.json"
        with open(json_path, "r", encoding="utf-8-sig") as f:
            movies = json.load(f)

        # 2. 读取本地海报文件夹，生成 电影标题:海报路径 映射表
        poster_dir = "../posters"  # 海报文件夹路径（根目录）
        poster_map = {}
        # 遍历所有海报文件
        if os.path.exists(poster_dir):
            for file in os.listdir(poster_dir):
                if file.endswith(".jpg"):
                    # 提取电影名（去掉后缀）
                    movie_title = file.replace(".jpg", "")
                    # 存储相对路径
                    poster_map[movie_title] = f"posters/{file}"

        # 3. 遍历电影，自动匹配海报路径
        for movie in movies:
            item = MovieItem()
            # 基础字段（和之前完全一致）
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

            # ✅ 核心：自动匹配本地海报路径（不用管顺序，按标题匹配）
            item["poster_url"] = poster_map.get(item["title"], "")

            if not item["rank"]:
                self.logger.warning(f"跳过空排名电影：{item['title']}")
                continue

            yield item