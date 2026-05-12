# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# --------------------- 1. 读取数据 ---------------------
df = pd.read_json("douban_top250_scrapy.json")
print("数据读取成功！共", len(df), "条电影")

# --------------------- 2. 数据清洗 ---------------------
df = df.drop_duplicates(subset="title")
df['score'] = df['score'].astype(float)
df['vote_num'] = df['vote_num'].fillna(0).astype(int)
print("清洗完成！")

# --------------------- 3. 分析1：评分最高TOP10 ---------------------
print("\n===== 评分最高TOP10 =====")
top10 = df.sort_values('score', ascending=False).head(10)
print(top10[['title', 'score', 'year']])

# --------------------- 可视化1：评分分布 ---------------------
plt.figure(figsize=(14, 6))

# 统计每个评分有多少部电影
score_count = df['score'].value_counts().sort_index()

plt.bar(score_count.index.astype(str), score_count.values, color='skyblue', edgecolor='black')

plt.title("豆瓣TOP250电影各评分数量分布", fontsize=14)
plt.xlabel("电影评分")
plt.ylabel("电影数量")
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

plt.savefig("score_count_clear.png", dpi=300)
plt.show()

# ---------------------  可视化2：年份趋势线图 ---------------------
year_count = df['year'].value_counts().sort_index()
plt.figure(figsize=(12,5))
year_count.plot(kind='line', color='red', marker='o')
plt.title("豆瓣TOP250电影上映年份趋势")
plt.xlabel("年份")
plt.ylabel("电影数量")
plt.xticks(rotation=45)
plt.grid(linestyle='--', alpha=0.7)
plt.savefig("year_trend.png", dpi=300, bbox_inches='tight')
plt.show()

# --------------------- 可视化3：电影类型分布饼图 ---------------------
import seaborn as sns

genre_list = []
for genres in df['genre']:
    if pd.notna(genres):
        genre_list.extend(genres.split('/'))
df_genre = pd.Series(genre_list).value_counts().reset_index()
df_genre.columns = ['genre', 'count']

total = df_genre['count'].sum()
df_genre['percent'] = df_genre['count'] / total * 100
main_genres = df_genre[df_genre['percent'] >= 2]
other_genres = df_genre[df_genre['percent'] < 2]


other_count = other_genres['count'].sum()
if other_count > 0:
    main_genres = pd.concat([main_genres, pd.DataFrame([{'genre': '其他', 'count': other_count}])], ignore_index=True)

plt.figure(figsize=(10, 8))
wedges, texts, autotexts = plt.pie(
    main_genres['count'],
    labels=main_genres['genre'],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('pastel', len(main_genres)),
    textprops={'fontsize': 10}  # 调整标签字体大小
)

for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_color('black')

plt.title("豆瓣TOP250电影类型分布（占比≥2%）", fontsize=14)
plt.savefig("genre_pie_optimized.png", dpi=300, bbox_inches='tight')
plt.show()


# --------------------- 可视化4：评分与评价人数相关性散点图 ---------------------
plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=df,
    x='score',
    y='vote_num',
    hue='score',
    palette='coolwarm',
    s=120,
    alpha=0.7,
    edgecolor='white'
)

corr = df['score'].corr(df['vote_num'])

plt.text(
    0.03, 0.95,
    f'相关系数 r = {corr:.2f}',
    transform=plt.gca().transAxes,
    fontsize=13,
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
)

plt.title('电影评分与评价人数相关性散点图', fontsize=15, pad=15)
plt.xlabel('豆瓣评分', fontsize=12)
plt.ylabel('评价人数（人）', fontsize=12)
plt.grid(linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('score_vote_scatter.png', dpi=300)
plt.show()
print(f"\n✅ 评分与评价人数的皮尔逊相关系数：{corr:.2f}")

# --------------------- 5. 可视化5：短评词云   ---------------------
from wordcloud import WordCloud
import jieba

import pymysql
conn = pymysql.connect(host='localhost', user='root', password='2006317', database='douban_movie', charset='utf8mb4')
df_comments = pd.read_sql("SELECT * FROM comments", conn)
conn.close()

all_comments = ' '.join(df_comments['content'].dropna().astype(str))
word_list = jieba.cut(all_comments)
word_str = ' '.join(word_list)

# 生成词云
wc = WordCloud(
    background_color='white',
    width=1000,
    height=800,
    font_path='simhei.ttf',
    max_words=200,
    max_font_size=100,
    stopwords={'的', '是', '了', '我', '很', '也', '就', '不', '都', '这', '一个', '没有', '可以', '就是', '还是', '这个', '时候', '什么', '一点', '一部', '因为', '如果', '这样', '那么', '可能', '还是', '不过', '其实', '自己', '不是', '知道', '觉得', '看到', '现在', '一直', '很多', '所以', '但是', '而且', '虽然', '还是', '只是', '已经', '一些', '一点', '没有', '这种', '那个', '一样', '真的', '这样', '很多', '一点', '一点', '一点'}
)
wc.generate(word_str)

plt.figure(figsize=(12, 10))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("豆瓣TOP250短评词云")
plt.savefig("comment_wordcloud.png", dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ 数据分析与可视化全部完成！")


# --------------------- 加分项：短评情感倾向分析 ---------------------
from snownlp import SnowNLP
import jieba
import pandas as pd
import matplotlib.pyplot as plt
import pymysql

# 1. 配置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 2. 从数据库读取短评数据
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='2006317',
    database='douban_movie',
    charset='utf8mb4'
)
df_comments = pd.read_sql("SELECT * FROM comments", conn)
conn.close()

# 3. 数据清洗：去除空评论和过短评论
df_comments = df_comments.dropna(subset=['content'])
df_comments = df_comments[df_comments['content'].str.len() > 2]
print(f"✅ 有效短评数量：{len(df_comments)} 条")

# 4. 情感分析
def analyze_sentiment(text):
    s = SnowNLP(text)
    return s.sentiments

df_comments['sentiment_score'] = df_comments['content'].apply(analyze_sentiment)

# 5. 按分数分类
def sentiment_category(score):
    if score > 0.6:
        return '正面'
    elif score < 0.4:
        return '负面'
    else:
        return '中性'

df_comments['sentiment_category'] = df_comments['sentiment_score'].apply(sentiment_category)

# 6. 统计结果
sentiment_count = df_comments['sentiment_category'].value_counts()
sentiment_ratio = df_comments['sentiment_category'].value_counts(normalize=True) * 100

print("\n===== 短评情感倾向统计 =====")
print(sentiment_count)
print("\n各类情感占比：")
print(sentiment_ratio.round(2))

# 7. 可视化：情感分布饼图
plt.figure(figsize=(8, 8))
colors = ['#66b3ff', '#ff9999', '#99ff99']
plt.pie(
    sentiment_count,
    labels=sentiment_count.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    textprops={'fontsize': 12}
)
plt.title("豆瓣TOP250电影短评情感倾向分布", fontsize=14)
plt.savefig("sentiment_pie.png", dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ 短评情感分析完成！")