import os
import pymysql

# ---------------------- 配置信息（改成你自己的） ----------------------
# 数据库连接信息
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "2006317"  # 改成你自己的MySQL密码
DB_NAME = "douban_movie"

# 海报文件夹路径（如果脚本在项目根目录，就直接写"posters"）
POSTER_FOLDER = "./posters"
# --------------------------------------------------------------------

def update_poster_paths():
    # 连接数据库
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4"
    )
    cursor = conn.cursor()

    # 遍历海报文件夹里的所有jpg文件
    poster_files = os.listdir(POSTER_FOLDER)
    count = 0

    for file_name in poster_files:
        # 只处理jpg文件
        if not file_name.endswith(".jpg"):
            continue

        # 提取电影名（去掉.jpg后缀）
        movie_title = file_name.replace(".jpg", "")
        # 生成本地路径（相对路径，和你的项目结构一致）
        poster_path = f"posters/{file_name}"

        # 更新数据库里对应的电影记录
        sql = """
            UPDATE movies 
            SET poster_url = %s 
            WHERE title = %s
        """
        cursor.execute(sql, (poster_path, movie_title))

        if cursor.rowcount > 0:
            print(f"✅ 匹配成功：《{movie_title}》 → {poster_path}")
            count += 1
        else:
            print(f"⚠️ 未找到对应电影：《{movie_title}》，跳过")

    # 提交修改，关闭连接
    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n🎉 匹配完成！共更新 {count} 条电影的海报路径")

if __name__ == "__main__":
    update_poster_paths()