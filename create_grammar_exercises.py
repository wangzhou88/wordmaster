import sqlite3
import os
from datetime import datetime

def create_grammar_exercises_table():
    # 获取数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), "wordmaster.db")
    
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 创建语法练习表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grammar_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_type TEXT NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT NOT NULL,
            difficulty_level INTEGER,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 提交更改
        conn.commit()
        print("语法练习表创建成功")
        
        # 插入示例介词练习
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('介词', 'I go to school _____ Monday.', 'on', 'in', 'at', 'by', 'on', 1, '具体日期前用on')
        ''')
        
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('介词', 'The cat is hiding _____ the table.', 'on', 'under', 'in', 'at', 'under', 1, '桌子下面用under')
        ''')
        
        # 插入示例第三人称单数练习
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('第三人称单数', 'He _____ to music every day.', 'listen', 'listens', 'listening', 'listened', 'listens', 1, '第三人称单数动词要加s')
        ''')
        
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('第三人称单数', 'My sister _____ her homework in the evening.', 'do', 'does', 'doing', 'did', 'does', 1, '第三人称单数用does')
        ''')
        
        # 插入示例动词练习
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('动词', 'I _____ to swim when I was young.', 'use', 'used', 'using', 'uses', 'used', 1, '过去时用used')
        ''')
        
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('动词', 'She is _____ a letter to her friend.', 'write', 'writes', 'writing', 'wrote', 'writing', 1, '现在进行时用ing形式')
        ''')
        
        # 插入示例动名词练习
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('动名词', 'I enjoy _____ in the morning.', 'run', 'running', 'runs', 'ran', 'running', 1, 'enjoy后接动名词')
        ''')
        
        cursor.execute('''
        INSERT INTO grammar_exercises (exercise_type, question, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, explanation)
        VALUES ('动名词', 'Reading is my favorite _____.', 'activity', 'activities', 'active', 'actively', 'activity', 1, '动名词可作主语')
        ''')
        
        # 提交所有更改
        conn.commit()
        print("示例语法练习数据插入成功")
        
    except sqlite3.Error as e:
        print(f"数据库操作出错: {e}")
        conn.rollback()
    
    finally:
        # 关闭数据库连接
        conn.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    create_grammar_exercises_table()