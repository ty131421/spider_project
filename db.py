import pymysql
from settings import DB_CONFIG

def get_conn():
    return pymysql.connect(**DB_CONFIG)

def create_tables():
    conn = get_conn()
    cursor = conn.cursor()

    # 电影表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rank INT, title VARCHAR(255), title_en TEXT,
        score FLOAT, vote_num INT,
        director TEXT, actors TEXT, intro TEXT,
        year VARCHAR(20), duration VARCHAR(100), genre VARCHAR(100),
        imdb VARCHAR(50), url VARCHAR(255)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')

    # 短评表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT,
        user VARCHAR(100), score VARCHAR(20),
        content TEXT, comment_time VARCHAR(50),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')

    conn.commit()
    cursor.close()
    conn.close()

def insert_movie(data):
    conn = get_conn()
    cursor = conn.cursor()
    sql = '''INSERT INTO movies 
    (rank,title,title_en,score,vote_num,director,actors,intro,year,duration,genre,imdb,url)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(sql, (
        data["rank"], data["title"], data["title_en"],
        data["score"], data["vote_num"], data["director"],
        data["actors"], data["intro"], data["year"],
        data["duration"], data["genre"], data["imdb"], data["url"]
    ))
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id

def insert_comment(mid, c):
    conn = get_conn()
    cursor = conn.cursor()
    sql = "INSERT INTO comments (movie_id,user,score,content,comment_time) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sql, (mid, c["user"], c["score"], c["content"], c["time"]))
    conn.commit()
    cursor.close()
    conn.close()