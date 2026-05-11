import os
import time
import requests
from anti_spider import get_headers, random_sleep, log_error
from settings import RETRY_TIMES

POSTER_DIR = "posters"

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:100]

def download_poster(movie_title, poster_url, retry_times=RETRY_TIMES):
    if not poster_url:
        log_error(f"海报链接为空: {movie_title}")
        return None
    
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    filename = sanitize_filename(f"{movie_title}.jpg")
    filepath = os.path.join(POSTER_DIR, filename)
    
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        if file_size > 0:
            return filepath
    
    headers = {
        "User-Agent": get_headers()["User-Agent"],
        "Referer": "https://movie.douban.com/",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive"
    }
    
    try:
        for attempt in range(retry_times):
            try:
                resp = requests.get(poster_url, headers=headers, stream=True, timeout=15)
                if resp.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in resp.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    random_sleep()
                    return filepath
                elif resp.status_code in [403, 418, 429]:
                    wait_time = (attempt + 1) * 5
                    log_error(f"下载海报被拒绝 {resp.status_code}，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    log_error(f"下载海报失败，状态码: {resp.status_code}")
                    return None
            except requests.exceptions.Timeout:
                wait_time = (attempt + 1) * 2
                log_error(f"下载海报超时，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                continue
            except Exception as e:
                log_error(f"下载海报异常: {e}")
                if attempt < retry_times - 1:
                    time.sleep(2)
                continue
        log_error(f"下载海报 {poster_url} 失败，已重试 {retry_times} 次")
        return None
    except Exception as e:
        log_error(f"下载海报 {movie_title} 时发生错误: {e}")
        return None