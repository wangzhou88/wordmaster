import sqlite3

def verify_database():
    conn = sqlite3.connect('wordmaster.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="grammar_exercises"')
    result = cursor.fetchone()
    
    if result:
        print('语法练习表已创建')
        
        cursor.execute('PRAGMA table_info(grammar_exercises)')
        columns = cursor.fetchall()
        print('\n表结构:')
        for col in columns:
            print(f'  {col[1]} ({col[2]})')
        
        cursor.execute('SELECT exercise_type, COUNT(*) FROM grammar_exercises GROUP BY exercise_type')
        counts = cursor.fetchall()
        print('\n各类语法练习数量:')
        for count in counts:
            print(f'  {count[0]}: {count[1]}题')
            
        cursor.execute('SELECT DISTINCT exercise_type FROM grammar_exercises')
        types = cursor.fetchall()
        print('\n练习类型:')
        for t in types:
            print(f'  {t[0]}')
            
        print('\n示例题目:')
        cursor.execute('SELECT exercise_type, question, option_a, option_b, option_c, option_d, correct_answer FROM grammar_exercises LIMIT 3')
        questions = cursor.fetchall()
        for q in questions:
            print(f'\n类型: {q[0]}')
            print(f'题目: {q[1]}')
            print(f'A. {q[2]}  B. {q[3]}  C. {q[4]}  D. {q[5]}')
            print(f'答案: {q[6]}')
    else:
        print('语法练习表未找到')

    conn.close()

if __name__ == "__main__":
    verify_database()