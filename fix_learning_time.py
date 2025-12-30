#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复脚本：添加学习时间表到现有数据库
"""

import sqlite3
import os

def fix_database():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordmaster.db")
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return
    
    print(f"正在修复数据库: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查learning_time表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='learning_time'")
    if cursor.fetchone():
        print("learning_time表已存在")
    else:
        print("创建learning_time表...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_time (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE,
            review_time INTEGER DEFAULT 0,
            test_time INTEGER DEFAULT 0,
            total_time INTEGER DEFAULT 0,
            UNIQUE(user_id, date),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        print("learning_time表创建成功！")
    
    # 创建索引
    print("创建索引...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_learning_time_user ON learning_time(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_learning_time_date ON learning_time(date)")
    print("索引创建成功！")
    
    # 检查review_history表是否存在（之前可能已创建）
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='review_history'")
    if cursor.fetchone():
        print("review_history表已存在")
    else:
        print("创建review_history表...")
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
        print("review_history表创建成功！")
    
    conn.commit()
    conn.close()
    
    print("数据库修复完成！")

if __name__ == "__main__":
    fix_database()
