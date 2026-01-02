"""
WordMaster应用主文件 - BeeWare版本
使用Toga框架实现原生UI
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.audio_beeware import audio_manager
from utils.speech_recog_beeware import SpeechRecognizer

class WordMasterApp(toga.App):
    def __init__(self):
        super().__init__()
        self.speech_recognizer = SpeechRecognizer()
        
    def startup(self):
        """应用启动方法"""
        # 创建主容器
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # 应用标题
        title_label = toga.Label(
            'WordMaster - 英语学习应用',
            style=Pack(font_size=24, font_weight='bold', padding=(0, 10))
        )
        self.main_box.add(title_label)
        
        # 创建学习模式选择区域
        self.create_mode_selection()
        
        # 创建学习区域
        self.create_learning_area()
        
        # 创建音频控制区域
        self.create_audio_controls()
        
        # 创建主窗口
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.size = (800, 600)
        
        # 显示主窗口
        self.main_window.show()
    
    def create_mode_selection(self):
        """创建学习模式选择区域"""
        mode_frame = toga.Box(style=Pack(direction=ROW, padding=5))
        
        # 学习模式标题
        mode_label = toga.Label('学习模式:', style=Pack(padding=(0, 5)))
        mode_frame.add(mode_label)
        
        # 模式选择按钮
        self.vocabulary_btn = toga.Button(
            '词汇学习',
            on_press=self.start_vocabulary_mode,
            style=Pack(margin=5)
        )
        mode_frame.add(self.vocabulary_btn)
        
        self.pronunciation_btn = toga.Button(
            '发音练习',
            on_press=self.start_pronunciation_mode,
            style=Pack(margin=5)
        )
        mode_frame.add(self.pronunciation_btn)
        
        self.quiz_btn = toga.Button(
            '词汇测验',
            on_press=self.start_quiz_mode,
            style=Pack(margin=5)
        )
        mode_frame.add(self.quiz_btn)
        
        self.main_box.add(mode_frame)
    
    def create_learning_area(self):
        """创建学习区域"""
        learning_frame = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # 当前词汇显示
        self.current_word_label = toga.Label(
            '选择学习模式开始学习',
            style=Pack(font_size=18, padding=(0, 10))
        )
        learning_frame.add(self.current_word_label)
        
        # 词汇信息
        self.word_info_label = toga.Label(
            '词汇信息将在这里显示',
            style=Pack(font_size=14, padding=(0, 5))
        )
        learning_frame.add(self.word_info_label)
        
        # 进度显示
        self.progress_label = toga.Label(
            '学习进度: 0/0',
            style=Pack(font_size=12, padding=(0, 5))
        )
        learning_frame.add(self.progress_label)
        
        self.main_box.add(learning_frame)
    
    def create_audio_controls(self):
        """创建音频控制区域"""
        audio_frame = toga.Box(style=Pack(direction=ROW, padding=10))
        
        # 播放音频按钮
        self.play_btn = toga.Button(
            '🔊 播放发音',
            on_press=self.play_audio,
            style=Pack(margin=5)
        )
        audio_frame.add(self.play_btn)
        
        # 录音按钮
        self.record_btn = toga.Button(
            '🎤 练习发音',
            on_press=self.record_pronunciation,
            style=Pack(margin=5)
        )
        audio_frame.add(self.record_btn)
        
        # 重复按钮
        self.repeat_btn = toga.Button(
            '🔄 重复练习',
            on_press=self.repeat_practice,
            style=Pack(margin=5)
        )
        audio_frame.add(self.repeat_btn)
        
        self.main_box.add(audio_frame)
    
    def start_vocabulary_mode(self, widget):
        """开始词汇学习模式"""
        self.current_mode = 'vocabulary'
        self.current_word_label.text = '词汇学习模式'
        self.word_info_label.text = '正在加载词汇库...'
        self.progress_label.text = '学习进度: 0/10'
        print("启动词汇学习模式")
    
    def start_pronunciation_mode(self, widget):
        """开始发音练习模式"""
        self.current_mode = 'pronunciation'
        self.current_word_label.text = '发音练习模式'
        self.word_info_label.text = '选择词汇进行发音练习'
        self.progress_label.text = '练习进度: 0/0'
        print("启动发音练习模式")
    
    def start_quiz_mode(self, widget):
        """开始词汇测验模式"""
        self.current_mode = 'quiz'
        self.current_word_label.text = '词汇测验模式'
        self.word_info_label.text = '开始词汇测验'
        self.progress_label.text = '测验进度: 0/10'
        print("启动词汇测验模式")
    
    def play_audio(self, widget):
        """播放音频"""
        try:
            # 使用现有的音频管理器
            if hasattr(self, 'current_mode') and self.current_mode:
                audio_file = "data/audio/hello_en.wav"  # 示例音频文件
                if os.path.exists(audio_file):
                    audio_manager.play(audio_file)
                    print(f"播放音频: {audio_file}")
                else:
                    print("音频文件不存在")
            else:
                print("请先选择学习模式")
        except Exception as e:
            print(f"音频播放失败: {e}")
    
    def record_pronunciation(self, widget):
        """录音练习发音"""
        try:
            result = self.speech_recognizer.recognize_from_microphone()
            if result:
                self.word_info_label.text = f"识别结果: {result}"
                print(f"语音识别结果: {result}")
            else:
                self.word_info_label.text = "未识别到语音，请重试"
                print("语音识别失败")
        except Exception as e:
            print(f"录音练习失败: {e}")
    
    def repeat_practice(self, widget):
        """重复练习"""
        print("重复练习功能")
        # 实现重复练习逻辑

def main():
    """应用入口点"""
    return WordMasterApp('WordMaster', 'com.wordmaster.app')

if __name__ == '__main__':
    app = main()
    app.main_loop()