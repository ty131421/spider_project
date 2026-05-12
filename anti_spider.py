import random
import time
import logging

# 日志配置（任务五）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawl.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 随机User-Agent列表（无依赖）
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

# 随机请求头（带Referer，防403）
def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://movie.douban.com/top250",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": 'bid=QKPAUpVXvlU; '
                  'dbcl2="295045503:qtffwl02H5Q"; '
                  'ck=Zxao; '
                  '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1778575866%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D;'
                  ' _pk_id.100001.4cf6=ece000f667d39ae4.1778575866.; _pk_ses.100001.4cf6=1; push_noty_num=0; '
                  'push_doumail_num=0'
    }

# 随机延迟（任务五）
def random_sleep(min_delay=2, max_delay=5):
    sleep_time = random.uniform(min_delay, max_delay)
    time.sleep(sleep_time)

# 日志工具（任务五）
def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)