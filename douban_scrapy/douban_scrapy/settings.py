# Scrapy settings for douban_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "douban_scrapy"

SPIDER_MODULES = ["douban_scrapy.spiders"]
NEWSPIDER_MODULE = "douban_scrapy.spiders"

ADDONS = {}


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"


ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = True


COOKIES_ENABLED = True
# COOKIES_DEBUG = True

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


SPIDER_MIDDLEWARES = {
    # "douban_scrapy.middlewares.DoubanScrapySpiderMiddleware": 543,
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 700,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 590,
    "douban_scrapy.middlewares.DoubanScrapyDownloaderMiddleware": 543,
    # "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
}

# ===================== 重试配置 =====================
# 开启重试机制，应对豆瓣的临时封禁/403
RETRY_ENABLED = True
RETRY_TIMES = 3  # 重试次数
RETRY_HTTP_CODES = [403, 408, 500, 502, 503, 504]  # 需要重试的状态码

# ===================== 管道配置 =====================
ITEM_PIPELINES = {
    "douban_scrapy.pipelines.DoubanPipeline": 300,
    "douban_scrapy.pipelines.DoubanCSVPipeline": 301,
    "douban_scrapy.pipelines.DoubanJSONPipeline": 302,
}


AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 3  # 初始延迟
AUTOTHROTTLE_MAX_DELAY = 10  # 最大延迟
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # 目标并发
AUTOTHROTTLE_DEBUG = False  # 关闭调试（上线后）


# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 3600  # 缓存1小时
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = [403, 500]
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"


FEED_EXPORT_ENCODING = "utf-8"

TELNETCONSOLE_ENABLED = False

DOWNLOAD_TIMEOUT = 15

LOG_LEVEL = "INFO"
# LOG_FILE = "douban_scrapy.log"