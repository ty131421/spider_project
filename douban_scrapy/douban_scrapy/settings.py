# -*- coding: utf-8 -*-

# Scrapy settings for douban_scrapy project
BOT_NAME = 'douban_scrapy'
SPIDER_MODULES = ['douban_scrapy.spiders']
NEWSPIDER_MODULE = 'douban_scrapy.spiders'

# 遵守Robots协议
ROBOTSTXT_OBEY = True

# 并发控制
CONCURRENT_REQUESTS = 2
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True

# 反爬虫
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://movie.douban.com/top250',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# 异常处理与重试
RETRY_ENABLED = True
RETRY_TIMES = 3  # 失败自动重试3次
RETRY_HTTP_CODES = [403, 404, 500, 502, 503, 504]

# 日志记录
LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FILE = 'scrapy_crawl.log'
LOG_ENCODING = 'utf-8'

# 其他默认配置
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
ITEM_PIPELINES = {
   'douban_scrapy.pipelines.DoubanScrapyPipeline': 300,
}
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False
HTTPCACHE_ENABLED = False