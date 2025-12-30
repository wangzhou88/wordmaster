import speech_recognition as sr
import os
import tempfile
from pydub import AudioSegment

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def recognize_from_microphone(self, language="en-US", timeout=5):
        """
        从麦克风识别语音
        :param language: 语言代码 (默认: 'en-US' 英语)
        :param timeout: 超时时间(秒)
        :return: 识别的文本
        """
        try:
            with sr.Microphone() as source:
                # 调整麦克风灵敏度
                self.recognizer.adjust_for_ambient_noise(source)
                
                print("请说话...")
                try:
                    # 监听麦克风输入
                    audio = self.recognizer.listen(source, timeout=timeout)
                except sr.WaitTimeoutError:
                    print("监听超时，请重试")
                    return None
                
                print("正在识别...")
                
                # 使用Google语音识别
                try:
                    text = self.recognizer.recognize_google(audio, language=language)
                    print(f"识别结果: {text}")
                    return text.lower()
                except sr.UnknownValueError:
                    print("无法识别语音")
                    return None
                except sr.RequestError as e:
                    print(f"无法连接到Google语音识别服务: {e}")
                    return None
        except Exception as e:
            print(f"语音识别失败: {e}")
            return None
    
    def recognize_from_file(self, file_path, language="en-US"):
        """
        从音频文件识别语音
        :param file_path: 音频文件路径
        :param language: 语言代码 (默认: 'en-US' 英语)
        :return: 识别的文本
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"音频文件不存在: {file_path}")
                return None
            
            # 转换音频文件格式（如果需要）
            temp_file = None
            if not file_path.lower().endswith('.wav'):
                temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                temp_file.close()
                
                # 使用pydub转换格式
                audio = AudioSegment.from_file(file_path)
                audio.export(temp_file.name, format="wav")
                
                file_path = temp_file.name
            
            # 读取音频文件
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                
                # 使用Google语音识别
                try:
                    text = self.recognizer.recognize_google(audio, language=language)
                    print(f"识别结果: {text}")
                    return text.lower()
                except sr.UnknownValueError:
                    print("无法识别语音")
                    return None
                except sr.RequestError as e:
                    print(f"无法连接到Google语音识别服务: {e}")
                    return None
                finally:
                    # 删除临时文件
                    if temp_file and os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
        except Exception as e:
            print(f"语音识别失败: {e}")
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