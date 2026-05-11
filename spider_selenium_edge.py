from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from anti_spider import get_headers
import time

def get_driver():
    opt = Options()
    opt.add_argument("--headless=new")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--window-size=1920,1080")
    opt.add_argument(f"user-agent={get_headers()['User-Agent']}")
    return webdriver.Edge(options=opt)

def crawl_detail(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(4)

    detail_data = {
        "year": "未知",
        "genre": "未知",
        "duration": "未知",
        "imdb": "未知",
        "comments": []
    }

    # 上映年份
    try:
        year_elem = driver.find_element(By.XPATH, '//span[@property="v:initialReleaseDate"]')
        detail_data["year"] = year_elem.text.strip()[:4]
    except:
        pass

    # 类型
    try:
        genres = driver.find_elements(By.XPATH, '//span[@property="v:genre"]')
        detail_data["genre"] = "/".join([g.text.strip() for g in genres])
    except:
        pass

    # 片长
    try:
        duration_elem = driver.find_element(By.XPATH, '//span[@property="v:runtime"]')
        detail_data["duration"] = duration_elem.text.strip()
    except:
        pass

    # IMDb
    try:
        info_text = driver.find_element(By.ID, 'info').text
        if 'IMDb:' in info_text:
            imdb_str = info_text.split('IMDb:')[1].split('\n')[0].strip()
            if imdb_str:
                detail_data["imdb"] = imdb_str
    except:
        pass
    if detail_data["imdb"] == "未知":
        try:
            imdb_link = driver.find_element(By.XPATH, '//div[@id="info"]//a[contains(@href,"imdb.com/title/")]')
            detail_data["imdb"] = imdb_link.text.strip()
        except:
            pass

    # 使用 Selenium + 无头浏览器处理 JavaScript 动态加载
    # 点击"全部XXX条"链接进入短评列表页
    try:
        # 尝试找到"全部XXX条"链接
        all_comments_link = None
        try:
            # 选择器1：包含"全部"和"条"的链接
            all_comments_link = driver.find_element(By.XPATH, '//a[contains(text(),"全部") and contains(text(),"条")]')
        except:
            try:
                # 选择器2：在短评标题区域找链接
                all_comments_link = driver.find_element(By.XPATH, '//div[@id="comments"]/h2/span/a')
            except:
                try:
                    # 选择器3：包含"全部"的链接
                    all_comments_link = driver.find_element(By.XPATH, '//a[contains(text(),"全部")]')
                except:
                    pass
        
        if all_comments_link and all_comments_link.is_displayed():
            # 点击进入全部短评页面
            driver.execute_script("arguments[0].click();", all_comments_link)
            time.sleep(4)  # 等待页面加载
            
            # 获取前15条短评
            comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div.comment-item')[:15]
            
            for c in comment_elements:
                comment = {
                    "user": "匿名",
                    "score": "无评分",
                    "content": "",
                    "time": ""
                }
                try:
                    user_elem = c.find_element(By.CSS_SELECTOR, '.comment-info a')
                    comment["user"] = user_elem.text.strip()
                except:
                    try:
                        comment["user"] = c.find_element(By.CLASS_NAME, "comment-info").text.split("\n")[0].strip()
                    except:
                        pass
                try:
                    score_elem = c.find_element(By.CSS_SELECTOR, '.comment-info span[title]')
                    comment["score"] = score_elem.get_attribute("title")
                except:
                    try:
                        score_elem = c.find_element(By.XPATH, './/span[contains(@class,"rating")]')
                        comment["score"] = score_elem.get_attribute("title")
                    except:
                        pass
                try:
                    comment["content"] = c.find_element(By.CLASS_NAME, "short").text.strip()
                except:
                    pass
                try:
                    comment["time"] = c.find_element(By.CLASS_NAME, "comment-time").text.strip()
                except:
                    pass
                detail_data["comments"].append(comment)
        else:
            # 如果找不到"全部"链接，使用原来的方法
            comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div.comment-item')[:15]
            for c in comment_elements:
                comment = {
                    "user": "匿名",
                    "score": "无评分",
                    "content": "",
                    "time": ""
                }
                try:
                    user_elem = c.find_element(By.CSS_SELECTOR, '.comment-info a')
                    comment["user"] = user_elem.text.strip()
                except:
                    pass
                try:
                    score_elem = c.find_element(By.CSS_SELECTOR, '.comment-info span[title]')
                    comment["score"] = score_elem.get_attribute("title")
                except:
                    pass
                try:
                    comment["content"] = c.find_element(By.CLASS_NAME, "short").text.strip()
                except:
                    pass
                try:
                    comment["time"] = c.find_element(By.CLASS_NAME, "comment-time").text.strip()
                except:
                    pass
                detail_data["comments"].append(comment)
            
    except Exception as e:
        pass

    driver.quit()
    return detail_data