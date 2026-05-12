import requests
from bs4 import BeautifulSoup
from anti_spider import get_headers, random_sleep, log_info, log_error
from settings import PAGE_COUNT, RETRY_TIMES, DELAY_MIN, DELAY_MAX
from tqdm import tqdm
import time

BASE_URL = "https://movie.douban.com/top250?start={}"

# 获取页面（带重试+异常处理+反爬，任务五核心）
def get_page(url):
    headers = get_headers()
    for attempt in range(RETRY_TIMES):
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                log_info(f"爬取成功：{url}")
                random_sleep(DELAY_MIN, DELAY_MAX)
                return resp.text
            elif resp.status_code == 403:
                wait_time = (attempt + 1) * 5
                log_error(f"403被拦截，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                log_error(f"状态码错误：{resp.status_code}，URL：{url}")
        except Exception as e:
            log_error(f"第{attempt+1}次失败：{str(e)}")
            time.sleep(3)
    log_error(f"爬取失败：{url}")
    return None

# 解析页面（完全保留你原来的逻辑）
def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    movie_items = soup.find_all("div", class_="item")
    movies = []

    for item in movie_items:
        rank = item.find("em").text.strip()
        title_cn = item.find_all("span", class_="title")[0].text.strip()
        title_en = ""
        if len(item.find_all("span", class_="title")) > 1:
            title_en = item.find_all("span", class_="title")[1].text.strip().lstrip("/").strip()

        rating = item.find("span", class_="rating_num").text.strip()
        vote_num = 0
        for span in item.find("div", class_="bd").find("div").find_all("span"):
            if "人评价" in span.text:
                vote_num = int(span.text.replace("人评价", "").replace(",", ""))
                break

        intro = ""
        quote = item.find("p", class_="quote")
        if quote:
            intro = quote.find("span").text.strip()

        director = ""
        actors = ""
        info_p = item.find("div", class_="bd").p
        if info_p:
            info_text = info_p.text.strip()
            if "导演:" in info_text:
                director = info_text.split("导演:")[1].split("主演:")[0].strip()
            if "主演:" in info_text:
                actors = info_text.split("主演:")[1].split("\n")[0].strip()

        link = item.find("a")["href"]
        poster_url = item.find("div", class_="pic").find("img")["src"]

        movies.append({
            "rank": int(rank),
            "title": title_cn,
            "title_en": title_en,
            "score": float(rating),
            "vote_num": vote_num,
            "director": director,
            "actors": actors,
            "intro": intro,
            "url": link,
            "poster_url": poster_url
        })
    return movies

# 主爬取函数（带进度条，任务五）
def crawl_top250():
    all_movies = []
    print("✅ 任务五已启动：反爬、日志、重试、延迟、进度条均生效")
    for i in tqdm(range(PAGE_COUNT), desc="爬取进度"):
        url = BASE_URL.format(i * 25)
        html = get_page(url)
        if html:
            all_movies.extend(parse(html))
    print(f"🎉 爬取完成，共 {len(all_movies)} 条数据")
    return all_movies

if __name__ == "__main__":
    crawl_top250()