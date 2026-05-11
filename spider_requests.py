import requests
from bs4 import BeautifulSoup
from anti_spider import get_headers, random_sleep, log_error
from settings import PAGE_COUNT, RETRY_TIMES
import time

BASE_URL = "https://movie.douban.com/top250?start={}"

def get_page(url, retry_times=RETRY_TIMES):
    headers = get_headers()
    for attempt in range(retry_times):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                random_sleep()
                return resp.text
            elif resp.status_code in [403, 429]:
                wait_time = (attempt + 1) * 5
                log_error(f"请求被拒绝 {resp.status_code}，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                continue
            else:
                log_error(f"请求失败，状态码: {resp.status_code}")
                return None
        except requests.exceptions.Timeout:
            wait_time = (attempt + 1) * 3
            log_error(f"请求超时，等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
            continue
        except Exception as e:
            log_error(f"请求异常: {e}")
            if attempt < retry_times - 1:
                time.sleep(2)
            continue
    log_error(f"请求 {url} 失败，已重试 {retry_times} 次")
    return None

def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all("div", class_="item")
    res = []

    for item in items:
        # 1 排名
        rank = item.find("em").text.strip()

        # 2 标题（中英）
        title_spans = item.find_all("span", class_="title")
        title = title_spans[0].text.strip() if title_spans else ""
        title_en = ""
        
        if len(title_spans) > 1:
            second_title = title_spans[1].text.strip().lstrip("/").strip()
            # 判断是否是英文标题（不含中文）
            if not any('\u4e00' <= c <= '\u9fff' for c in second_title):
                title_en = second_title
        
        # 如果title_en还是空的，从other中提取
        if not title_en:
            other = item.find("span", class_="other")
            if other:
                other_text = other.text.strip().lstrip("/").strip()
                # 分割别名，找英文部分
                parts = [p.strip() for p in other_text.split("/") if p.strip()]
                for part in parts:
                    if part and not any('\u4e00' <= c <= '\u9fff' for c in part):
                        title_en = part
                        break

        # 3 评分
        rating = item.find("span", class_="rating_num").text.strip()

        # 评论人数
        vote_num = 0
        bd_div = item.find("div", class_="bd")
        if bd_div:
            rating_div = bd_div.find("div")
            if rating_div:
                vote_spans = rating_div.find_all("span")
                for span in vote_spans:
                    text = span.text.strip()
                    if "人评价" in text:
                        vote_num = int(text.replace("人评价", "").replace(",", ""))
                        break

        # 简介（从 quote 标签中获取）
        intro = ""
        quote_p = item.find("p", class_="quote")
        if quote_p:
            intro_span = quote_p.find("span")
            if intro_span:
                intro = intro_span.text.strip()

        # 导演 主演
        director = ""
        actors = ""
        info_p = item.find("div", class_="bd").p
        if info_p:
            info = info_p.text.strip()
            if "导演:" in info:
                director = info.split("导演:")[1].split("主演:")[0].strip()
            if "主演:" in info:
                actors = info.split("主演:")[1].split("\n")[0].strip()

        # 链接
        link = item.find("a")["href"]
        
        # 海报链接
        poster_url = ""
        pic_div = item.find("div", class_="pic")
        if pic_div:
            img_elem = pic_div.find("img")
            if img_elem and "src" in img_elem.attrs:
                poster_url = img_elem["src"]

        res.append({
            "rank": int(rank),
            "title": title,
            "title_en": title_en,
            "score": float(rating),
            "vote_num": vote_num,
            "director": director,
            "actors": actors,
            "intro": intro,
            "url": link,
            "poster_url": poster_url
        })

    return res

def crawl_top250():
    all_movies = []
    for i in range(PAGE_COUNT):
        url = BASE_URL.format(i * 25)
        html = get_page(url)
        if html:
            all_movies.extend(parse(html))
    return all_movies