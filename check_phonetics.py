#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

def check_phonetics():
    """检查数据库中的音标数据"""
    print('=' * 60)
    print('音标数据检查')
    print('=' * 60)
    
    # 数据库路径
    db_path = os.path.join(os.getcwd(), 'wordmaster.db')
    
    if not os.path.exists(db_path):
        print(f'数据库文件不存在: {db_path}')
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表结构
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f'数据库中的表: {[table[0] for table in tables]}')
        
        # 检查words表结构
        cursor.execute("PRAGMA table_info(words);")
        columns = cursor.fetchall()
        print(f'words表的列: {[col[1] for col in columns]}')
        
        # 获取一些有音标的单词示例
        cursor.execute("""
            SELECT w.word, w.phonetic, d.name as dictionary_name 
            FROM words w 
            JOIN dictionaries d ON w.dictionary_id = d.id 
            WHERE w.phonetic IS NOT NULL AND w.phonetic != ''
            ORDER BY w.word 
            LIMIT 20
        """)
        
        words = cursor.fetchall()
        
        print(f'\n找到 {len(words)} 个有音标的单词:')
        print('-' * 60)
        
        for word, phonetic, dict_name in words:
            # 应用格式化函数
            if phonetic:
                import re
                cleaned = phonetic.strip()
                cleaned = re.sub(r'^\[|\]$', '', cleaned)
                cleaned = re.sub(r'^["\']|["\']$', '', cleaned)
                formatted = cleaned
            else:
                formatted = ""
            
            print(f'{word:15} -> 原始: {phonetic}')
            print(f'{"":15}     格式化: {formatted}')
            print(f'{"":15}     词库: {dict_name}')
            print()
        
        # 检查音标格式分布
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN phonetic LIKE '[%' THEN '带方括号'
                    WHEN phonetic LIKE '["%' OR phonetic LIKE "['%" THEN '带引号'
                    WHEN phonetic LIKE '%]' THEN '带右括号'
                    ELSE '其他格式'
                END as format_type,
                COUNT(*) as count
            FROM words 
            WHERE phonetic IS NOT NULL AND phonetic != ''
            GROUP BY format_type
        """)
        
        format_stats = cursor.fetchall()
        print('音标格式分布:')
        for format_type, count in format_stats:
            print(f'  {format_type}: {count} 个')
        
        conn.close()
        
    except Exception as e:
        print(f'检查失败: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_phonetics()