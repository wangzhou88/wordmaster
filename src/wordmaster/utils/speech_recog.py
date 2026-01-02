import os
import tempfile
import shutil

# Simplified SpeechRecognizer for Android compatibility
class SpeechRecognizer:
    def __init__(self):
        # Using plyer for microphone access on Android
        try:
            from plyer import speech
            self.speech = speech
        except ImportError:
            self.speech = None
            print("语音识别不可用: 未找到speech模块")
    
    def recognize_from_microphone(self, language="en-US", timeout=5):
        """
        从麦克风识别语音
        :param language: 语言代码 (默认: 'en-US' 英语)
        :param timeout: 超时时间(秒)
        :return: 识别的文本
        """
        # This is a simplified implementation for Android
        # Real speech recognition would require additional services
        print("Android平台上的语音识别功能已简化")
        return None
    
    def recognize_from_file(self, file_path, language="en-US"):
        """
        从音频文件识别语音
        :param file_path: 音频文件路径
        :param language: 语言代码 (默认: 'en-US' 英语)
        :return: 识别的文本
        """
        # This is a simplified implementation for Android
        # Real speech recognition would require additional services
        print("Android平台上的语音识别功能已简化")
        return None
    
    def compare_with_text(self, recognized_text, expected_text):
        """
        比较识别的文本和预期文本
        :param recognized_text: 识别的文本
        :param expected_text: 预期文本
        :return: 是否匹配
        """
        if not recognized_text:
            return False
        
        # 转换为小写并去除空格
        recognized_text = recognized_text.lower().strip()
        expected_text = expected_text.lower().strip()
        
        # 完全匹配
        if recognized_text == expected_text:
            return True
        
        # 部分匹配（考虑可能的识别错误）
        # 例如："hello" 可能被识别为 "hallo"
        # 这里可以添加更复杂的匹配算法
        # 暂时使用简单的包含关系判断
        if expected_text in recognized_text or recognized_text in expected_text:
            return True
        
        return False

# 创建全局语音识别器实例
speech_recognizer = SpeechRecognizer()