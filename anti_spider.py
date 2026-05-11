import random
import time
import logging

logging.basicConfig(
    filename="crawl.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def random_sleep():
    time.sleep(random.uniform(1, 4))

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)