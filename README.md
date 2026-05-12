# 豆瓣电影Top250爬虫数据采集与分析系统

## 项目简介
基于Python的豆瓣电影Top250数据采集系统，支持列表页+详情页+短评多层级爬取，实现数据存储、清洗、分析与可视化。

## 📋 项目进度

### ✅ 已完成功能

#### 1. 基础爬取模块
- ✅ 爬取豆瓣Top250全量列表页（10页）
- ✅ 提取：排名、标题（中英）、评分、评价人数、导演/主演、简介、详情链接
- ✅ 智能分页（自动遍历10页）
- ✅ 随机User-Agent池（防止被封）
- ✅ 请求延时（随机1-4秒）
- ✅ 异常重试机制（超时/403/429等状态码）

#### 2. 进阶详情与动态爬取模块
- ✅ 使用Selenium + 无头浏览器（Edge）处理JavaScript动态加载
- ✅ 进入详情页提取：上映年份、片长、类型、IMDb评分
- ✅ 点击"全部"链接获取至少15条热门短评（含评论者、评分、内容、时间）
- ✅ 下载电影海报图片（支持断点续传）

#### 3. 数据存储
- ✅ MySQL双表存储：movies主表 + comments短评表（使用外键关联）
- ✅ CSV格式数据备份
- ✅ JSON格式数据备份

#### 3. 框架重构

- ✅ MySQL双表存储：movies主表 + comments短评表（使用外键关联）
- ✅ CSV格式数据备份
- ✅ JSON格式数据备份

- ✅ 使用Scrapy框架完整重构核心爬虫逻辑
- ✅ 实现Scrapy Item、Spider、Pipeline、Downloader Middleware
- ✅ requests与Scrapy性能对比分析

### ❌ 待完成功能

#### 4. 数据分析与可视化模块（待完成）
- ❌ 使用pandas进行数据清洗（缺失值处理、类型转换、去重）
- ❌ 统计分析：高分电影Top10、导演/类型分布、评分与评价人数相关性
- ❌ 可视化图表：评分分布直方图、类型饼图、散点图、短评词云、时间趋势线图
- ❌ 短评情感分析（jieba分词 + SnowNLP）

#### 5. 反爬虫、优化与工程实践（待完成）
- ❌ 实现免费代理IP池轮换
- ❌ Cookie管理、随机Headers
- ❌ 检查并记录Robots.txt遵守情况
- ❌ 性能优化：多线程/异步或Scrapy并发控制
- ❌ 完善日志记录（logging模块）

## 🛠️ 技术栈

| 模块 | 技术 | 版本 |
|------|------|------|
| 基础爬取 | requests | >=2.31.0 |
| HTML解析 | BeautifulSoup4 | >=4.12.0 |
| 动态页面 | Selenium | >=4.17.0 |
| 数据库 | PyMySQL | >=1.1.0 |
| 进度显示 | tqdm | >=4.66.0 |

## 📁 项目结构

```
douban_project/
├── spider_requests.py          # requests基础爬取模块（列表页）
├── spider_selenium_edge.py     # Selenium动态爬取模块（详情页+短评）
├── poster_downloader.py        # 海报下载模块（支持断点续传）
├── run_spider.py              # 主运行脚本
├── db.py                      # MySQL数据库操作（建表、插入、查询）
├── anti_spider.py             # 反爬虫配置（User-Agent池、随机延时）
├── settings.py                # 配置文件（数据库连接等）
├── requirements.txt           # Python依赖列表
├── douban_top250.csv          # CSV格式数据备份
├── douban_top250.json         # JSON格式数据备份
├── douban_movie.sql           # MySQL数据库备份
├── crawl.log                  # 爬取日志
└── posters/                   # 海报图片目录（运行后自动生成）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

修改 `settings.py` 中的数据库连接信息：

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "douban_movie",
    "port": 3307,
    "charset": "utf8mb4"
}
```

### 3. 创建数据库

```sql
CREATE DATABASE IF NOT EXISTS douban_movie DEFAULT CHARACTER SET utf8mb4;
```

### 4. 运行爬虫

```bash
python run_spider.py
```

## 📊 数据说明

### movies表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键自增 |
| rank | INT | 排名 |
| title | VARCHAR | 中文标题 |
| title_en | VARCHAR | 英文标题 |
| score | FLOAT | 评分 |
| vote_num | INT | 评价人数 |
| director | VARCHAR | 导演 |
| actors | VARCHAR | 主演 |
| intro | TEXT | 简介 |
| year | VARCHAR | 上映年份 |
| genre | VARCHAR | 类型 |
| duration | VARCHAR | 片长 |
| imdb | VARCHAR | IMDb编号 |
| url | VARCHAR | 详情链接 |
| poster_url | VARCHAR | 海报链接 |

### comments表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键自增 |
| movie_id | INT | 电影ID（外键关联movies.id） |
| user | VARCHAR | 评论者 |
| score | VARCHAR | 评分 |
| content | TEXT | 短评内容 |
| comment_time | VARCHAR | 评论时间 |

## 👥 团队分工

| 成员 | 负责模块 | 完成进度 |
|------|----------|----------|
| 成员A | 基础requests爬取、Selenium动态处理、海报下载、反爬策略 | ✅ 已完成 |
| 成员B | Scrapy框架重构、MySQL存储Pipeline、数据清洗、日志异常处理 | ❌ 待完成 |
| 成员C | 数据分析、可视化图表、情感分析、报告整合、Git仓库管理 | ❌ 待完成 |

## 📝 运行截图

### 爬取过程
```
正在创建数据库表...
开始爬取豆瓣TOP250列表...
开始爬取详情页与短评...
100%|████████████████████████████████| 250/250 [1:30:00<00:00, 21.60s/it]
数据已保存到数据库
数据已导出到 douban_top250.csv
数据已导出到 douban_top250.json
```

## ⚠️ 注意事项

1. 请确保MySQL服务已启动
2. 首次运行可能需要较长时间（约1.5-3小时），建议在空闲时间运行
3. 请遵守网站robots.txt规则，不要频繁爬取
4. 本项目仅供学习使用，请勿用于商业用途

## 📄 许可证

MIT License

---

**项目状态**：基础爬取功能已完成，正在进行Scrapy重构和数据分析模块开发