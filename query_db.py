import sqlite3

conn = sqlite3.connect('wordmaster.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('数据库中的表:')
for table in tables:
    print(f'  - {table[0]}')

print()

cursor.execute('PRAGMA table_info(dictionaries)')
print('dictionaries表结构:')
for col in cursor.fetchall():
    print(f'  {col}')

print()

cursor.execute('PRAGMA table_info(words)')
print('words表结构:')
for col in cursor.fetchall():
    print(f'  {col}')

print()

cursor.execute('SELECT id, name, description, word_count FROM dictionaries')
dictionaries = cursor.fetchall()
print('现有词库:')
for d in dictionaries:
    print(f'  ID:{d[0]} 名称:{d[1]} 说明:{d[2]} 单词数:{d[3]}')

print()

if dictionaries:
    dict_id = dictionaries[0][0]
    cursor.execute('SELECT id, word, translation, phonetic, definition, example FROM words WHERE dictionary_id = ? LIMIT 50', (dict_id,))
    words = cursor.fetchall()
    print(f'词库1的前50个单词:')
    for w in words:
        print(f'  {w[1]:20} - {w[2]}')

conn.close()
