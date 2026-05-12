import pymysql
import csv
import json
from douban_scrapy.items import MovieItem, CommentItem

class DoubanPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='2006317',
            database='douban_movie',
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            # 处理电影Item
            if isinstance(item, MovieItem):
                rank = int(item["rank"]) if item["rank"] else None
                score = float(item["score"]) if item["score"] else None
                vote_num = int(item["vote_num"]) if item["vote_num"] else None

                sql = """
                INSERT INTO movies (
                    `rank`, title, title_en, score, vote_num, director, actors, intro,
                    year, duration, genre, imdb_id, url, poster_url
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    score=VALUES(score), vote_num=VALUES(vote_num)
                """

                self.cursor.execute(sql, (
                    rank,
                    item["title"],
                    item.get("title_en", ""),
                    score,
                    vote_num,
                    item.get("director", ""),
                    item.get("actors", ""),
                    item.get("intro", ""),
                    item.get("year", ""),
                    item.get("duration", ""),
                    item.get("genre", ""),
                    item.get("imdb", ""),
                    item["url"],
                    item.get("poster_url", "")
                ))
                self.conn.commit()
                spider.logger.info(f"✅ 成功存入电影：第{rank}名 {item['title']}")

            # 处理短评Item
            elif isinstance(item, CommentItem):
                movie_id = int(item["movie_id"]) if item["movie_id"] else None

                sql = """
                INSERT INTO comments (
                    movie_id, user_name, comment_score, comment_content, comment_time
                ) VALUES (%s,%s,%s,%s,%s)
                """

                self.cursor.execute(sql, (
                    movie_id,
                    item.get("user_name", ""),
                    item.get("comment_score", ""),
                    item.get("comment_content", ""),
                    item.get("comment_time", "")
                ))
                self.conn.commit()
                spider.logger.info(f"✅ 成功存入短评：电影ID {movie_id}")

        except Exception as e:
            spider.logger.error(f"❌ 存储失败：{e}，数据：{item}")
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        spider.logger.info("🔌 数据库连接已关闭")

class DoubanCSVPipeline:
    def __init__(self):
        self.file = open('douban_top250_scrapy.csv', 'w', encoding='utf-8-sig', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=[
            'rank', 'title', 'title_en', 'score', 'vote_num', 'director',
            'actors', 'intro', 'year', 'duration', 'genre', 'imdb', 'url', 'poster_url'
        ])
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        self.file.close()

# 新增JSON备份管道
class DoubanJSONPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        with open('douban_top250_scrapy.json', 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)