#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试发音和音标功能"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import format_phonetic
import sqlite3

def test_phonetic_format():
    """测试音标格式化"""
    print('=' * 50)
    print('音标格式化测试')
    print('=' * 50)
    
    test_cases = [
        ("['klɑːsrʊm]", "klɑːsrʊm"),
        ("['wɪndəʊ]", "wɪndəʊ"),
        ("['blækbɔːd]", "blækbɔːd"),
        ("[laɪt]", "laɪt"),
        ("['pɪktʃə]", "pɪktʃə"),
        (None, ""),
        ("", ""),
        ("[test]", "test"),
    ]
    
    all_passed = True
    for input_val, expected in test_cases:
        result = format_phonetic(input_val)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f'{status} 输入: {input_val!r:20} -> 输出: {result!r:15} (预期: {expected!r})')
    
    print()
    return all_passed

def test_database_phonetics():
    """测试数据库中的音标"""
    print('=' * 50)
    print('数据库音标测试')
    print('=' * 50)
    
    try:
        conn = sqlite3.connect('wordmaster.db')
        cursor = conn.cursor()
        cursor.execute('SELECT word, phonetic FROM words LIMIT 10')
        rows = cursor.fetchall()
        conn.close()
        
        for word, phonetic in rows:
            formatted = format_phonetic(phonetic)
            print(f'  {word:20} -> {formatted}')
        
        print()
        return True
    except Exception as e:
        print(f'数据库测试失败: {e}')
        return False

def test_audio_system():
    """测试音频系统"""
    print('=' * 50)
    print('音频系统测试')
    print('=' * 50)
    
    try:
        from utils.audio import audio_manager
        
        # 测试生成一个单词的音频
        test_word = 'hello'
        
        # 清理旧的音频文件
        audio_dir = audio_manager.audio_dir
        old_files = [f for f in os.listdir(audio_dir) if test_word.lower() in f.lower() or 'hello' in f.lower()]
        for old_file in old_files:
            old_path = os.path.join(audio_dir, old_file)
            try:
                os.remove(old_path)
                print(f'已清理旧文件: {old_path}')
            except:
                pass
        
        print(f'正在为单词 "{test_word}" 生成音频...')
        
        audio_path = audio_manager.get_word_audio_path(test_word)
        
        if audio_path and os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f'✓ 音频文件创建成功: {audio_path}')
            print(f'  文件大小: {file_size} bytes')
            
            if file_size == 0:
                print('✗ 音频文件为空，测试失败')
                return False
            
            # 测试播放
            print(f'正在测试播放...')
            success = audio_manager.play_audio(audio_path)
            if success:
                print('✓ 音频播放成功')
            else:
                print('✗ 音频播放失败')
            
            return success
        else:
            print('✗ 音频文件创建失败')
            return False
    except Exception as e:
        print(f'音频系统测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False

def main():
    print()
    print('单词大师 - 发音和音标功能测试')
    print()
    
    results = []
    
    # 测试音标格式化
    results.append(('音标格式化', test_phonetic_format()))
    
    # 测试数据库音标
    results.append(('数据库音标', test_database_phonetics()))
    
    # 测试音频系统
    results.append(('音频系统', test_audio_system()))
    
    # 总结
    print('=' * 50)
    print('测试总结')
    print('=' * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = '✓ 通过' if passed else '✗ 失败'
        print(f'  {test_name}: {status}')
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print('所有测试通过! ✓')
        return 0
    else:
        print('部分测试失败，请检查上述输出。')
        return 1

if __name__ == '__main__':
    sys.exit(main())
