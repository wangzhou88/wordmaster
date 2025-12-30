#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def test_fallback():
    """测试回退机制"""
    print('=' * 50)
    print('回退机制测试')
    print('=' * 50)
    
    try:
        from utils.audio import audio_manager
        
        # 测试单词
        test_word = 'test'
        
        # 清理旧文件
        audio_dir = audio_manager.audio_dir
        old_files = [f for f in os.listdir(audio_dir) if 'test' in f.lower()]
        for old_file in old_files:
            old_path = os.path.join(audio_dir, old_file)
            try:
                os.remove(old_path)
                print(f'已清理旧文件: {old_path}')
            except:
                pass
        
        print(f'正在为单词 "{test_word}" 生成音频（强制回退）...')
        
        # 强制生成回退音频（修改文件名以确保生成新的）
        fallback_filename = f'fallback_{test_word}_{int(time.time())}.wav'
        
        # 直接调用创建回退音频的方法
        fallback_path = audio_manager._create_fallback_beep(
            os.path.join(audio_dir, fallback_filename)
        )
        
        if fallback_path and os.path.exists(fallback_path):
            file_size = os.path.getsize(fallback_path)
            print(f'✓ 回退音频创建成功: {fallback_path}')
            print(f'  文件大小: {file_size} bytes')
            
            if file_size > 0:
                print('✓ 回退音频文件不为空')
                
                # 测试播放
                print('正在测试播放回退音频...')
                success = audio_manager.play_audio(fallback_path)
                if success:
                    print('✓ 回退音频播放成功')
                else:
                    print('✗ 回退音频播放失败')
                
                return success
            else:
                print('✗ 回退音频文件为空')
                return False
        else:
            print('✗ 回退音频创建失败')
            return False
            
    except Exception as e:
        print(f'回退机制测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_fallback()