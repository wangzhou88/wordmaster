import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordmaster.db")

print(f"数据库路径: {db_path}")
print(f"数据库文件存在: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n现有表: {[t[0] for t in tables]}")

    if not any(t[0] == 'review_history' for t in tables):
        print("\n创建 review_history 表...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS review_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE,
            reviewed_count INTEGER DEFAULT 0,
            total_reviews INTEGER DEFAULT 0,
            avg_quality FLOAT DEFAULT 0,
            UNIQUE(user_id, date),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        conn.commit()
        print("review_history 表创建成功！")
    else:
        print("review_history 表已存在")

    if not any(t[0] == 'idx_review_history_user_date' for t in tables):
        print("\n创建索引...")
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_review_history_user_date ON review_history(user_id, date)")
            conn.commit()
            print("索引创建成功！")
        except Exception as e:
            print(f"索引已存在或创建失败: {e}")

    conn.close()
    print("\n修复完成！")
