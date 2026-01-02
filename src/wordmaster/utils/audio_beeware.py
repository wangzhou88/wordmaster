"""
音频管理器 - BeeWare版本
针对原生移动平台优化
"""

import os
import tempfile
import time
import threading
import wave
import struct
import shutil

# BeeWare平台音频支持
class AudioPlayer:
    _initialized = False
    _player = None
    
    @staticmethod
    def initialize():
        if AudioPlayer._initialized:
            return True
            
        try:
            # 在BeeWare中，我们可以使用plyer或者系统原生API
            # plyer在BeeWare平台上有更好的支持
            try:
                from plyer import audio
                AudioPlayer._player = audio
                AudioPlayer._initialized = True
                print("✅ 音频系统初始化成功 (BeeWare + plyer)")
                return True
            except ImportError:
                print("⚠️ plyer不可用，使用系统音频API")
                # 可以在这里添加系统原生音频API调用
                AudioPlayer._player = None
                AudioPlayer._initialized = True
                return True
        except Exception as e:
            print(f"❌ 初始化音频系统失败: {e}")
            return False
    
    @staticmethod
    def play(file_path):
        """播放音频文件"""
        if not AudioPlayer._initialized:
            AudioPlayer.initialize()
        
        if not AudioPlayer._player:
            print("⚠️ 音频系统未就绪")
            return False
        
        try:
            # 确保文件存在
            if not os.path.exists(file_path):
                print(f"❌ 音频文件不存在: {file_path}")
                return False
            
            # 使用plyer播放音频
            AudioPlayer._player.play(file_path)
            print(f"✅ 播放音频: {os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            print(f"❌ 音频播放失败: {e}")
            return False
    
    @staticmethod
    def stop():
        """停止音频播放"""
        try:
            if AudioPlayer._player:
                AudioPlayer._player.stop()
                print("✅ 音频播放已停止")
        except Exception as e:
            print(f"⚠️ 停止音频播放时出错: {e}")
    
    @staticmethod
    def set_volume(volume):
        """设置音量 (0.0 - 1.0)"""
        try:
            if AudioPlayer._player and hasattr(AudioPlayer._player, 'set_volume'):
                AudioPlayer._player.set_volume(volume)
                print(f"✅ 音量设置为: {volume}")
        except Exception as e:
            print(f"⚠️ 设置音量时出错: {e}")

# 全局音频管理器实例
audio_manager = AudioPlayer()

# 保持向后兼容
class AudioManager:
    @staticmethod
    def play(file_path):
        return AudioPlayer.play(file_path)
    
    @staticmethod
    def stop():
        return AudioPlayer.stop()
    
    @staticmethod
    def initialize():
        return AudioPlayer.initialize()

# 为了兼容现有代码，提供全局实例
audio_manager = AudioManager()