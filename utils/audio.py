import os
import tempfile
import time
import threading
import wave
import struct
import shutil
from gtts import gTTS
import pygame
from pygame import mixer

class AudioManager:
    _instance = None
    
    def __new__(cls, audio_dir=None):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, audio_dir=None):
        if self._initialized:
            return
        
        if audio_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.audio_dir = os.path.join(base_dir, 'data', 'audio')
        else:
            self.audio_dir = audio_dir
        
        os.makedirs(self.audio_dir, exist_ok=True)
        
        self._tts_cache = {}
        self._loading_words = set()
        self._initialized = True
        
        self._reinit_audio()
    
    def _reinit_audio(self):
        try:
            if not pygame.get_init():
                pygame.init()
            
            mixer.quit()
            mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
            print("音频系统初始化成功")
        except Exception as e:
            print(f"初始化音频系统失败: {e}")
            try:
                mixer.init(frequency=16000, size=-16, channels=1, buffer=512)
                print("使用备用音频配置初始化成功")
            except:
                pass
    
    def _ensure_audio(self):
        try:
            if not pygame.get_init():
                pygame.init()
            
            if not mixer.get_init():
                try:
                    mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
                except:
                    mixer.init(frequency=16000, size=-16, channels=1, buffer=512)
            
            return True
        except Exception as e:
            print(f"音频系统检查失败: {e}")
            return False
    
    def _create_wav_file(self, file_path, frequency=440, duration=0.5):
        try:
            sample_rate = 22050
            n_samples = int(sample_rate * duration)
            
            with wave.open(file_path, 'w') as wave_file:
                wave_file.setnchannels(1)
                wave_file.setsampwidth(2)
                wave_file.setframerate(sample_rate)
                
                for i in range(n_samples):
                    t = i / sample_rate
                    envelope = 1.0
                    if t < 0.05:
                        envelope = t / 0.05
                    elif t > duration - 0.05:
                        envelope = (duration - t) / 0.05
                    
                    value = int(32767.0 * 0.5 * envelope * (1 + 0.3 * (i / n_samples)))
                    wave_file.writeframes(struct.pack('<h', value))
            
            return file_path
        except Exception as e:
            print(f"创建备用提示音失败: {e}")
            return None
    
    def text_to_speech(self, text, language='en', filename=None):
        if not text or not text.strip():
            return None
        
        text = text.strip()
        cache_key = f"{text}_{language}"
        
        if cache_key in self._tts_cache:
            cached_path = self._tts_cache[cache_key]
            if cached_path and os.path.exists(cached_path):
                return cached_path
        
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            
            if filename is None:
                filename = f"{hash(text)}_{int(time.time())}.wav"
            elif not filename.endswith('.wav'):
                filename = filename.rsplit('.', 1)[0] + '.wav'
            
            file_path = os.path.join(self.audio_dir, filename)
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                tts.save(tmp_path)
                
                if not os.path.exists(tmp_path):
                    raise Exception("gTTS未能生成文件")
                
                file_size = os.path.getsize(tmp_path)
                if file_size < 100:
                    os.remove(tmp_path)
                    raise Exception("生成的音频文件过小")
                
                self._convert_to_wav(tmp_path, file_path)
                os.remove(tmp_path)
                
            except Exception as e:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                raise e
            
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > 0:
                    self._tts_cache[cache_key] = file_path
                    return file_path
            
            raise Exception("音频文件无效")
                
        except Exception as e:
            print(f"TTS生成失败: {e}")
            
            if filename is None:
                filename = f"{hash(text)}_{int(time.time())}.wav"
            else:
                filename = filename.rsplit('.', 1)[0] + '.wav'
            
            file_path = os.path.join(self.audio_dir, filename)
            result = self._create_wav_file(file_path)
            if result:
                self._tts_cache[cache_key] = result
            return result
    
    def _convert_to_wav(self, mp3_path, wav_path):
        try:
            from pydub import AudioSegment
            sound = AudioSegment.from_mp3(mp3_path)
            sound.export(wav_path, format="wav")
        except Exception as e:
            print(f"转换MP3到WAV失败: {e}")
            if not wav_path.endswith('.wav'):
                wav_path = wav_path.rsplit('.', 1)[0] + '.wav'
            shutil.copy(mp3_path, wav_path)
    
    def play_audio(self, file_path):
        if not file_path or not os.path.exists(file_path):
            print(f"音频文件不存在: {file_path}")
            return False
        
        if not self._ensure_audio():
            print("音频系统未就绪")
            return False
        
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                print(f"音频文件为空: {file_path}")
                return False
            
            mixer.music.load(file_path)
            mixer.music.play()
            
            return True
        except Exception as e:
            print(f"音频播放失败: {e}")
            return False
    
    def play_audio_nonblocking(self, file_path):
        return self.play_audio(file_path)
    
    def stop_audio(self):
        try:
            if mixer.get_init():
                mixer.music.stop()
        except:
            pass
    
    def preload_word_audio(self, word, language='en'):
        if not word:
            return
        
        word = word.strip()
        if not word:
            return
        
        cache_key = f"{word}_{language}"
        if cache_key in self._loading_words:
            return
        
        self._loading_words.add(cache_key)
        
        def _preload():
            try:
                filename = f"{word.lower().replace(' ', '_')}_{language}.wav"
                file_path = os.path.join(self.audio_dir, filename)
                
                if not os.path.exists(file_path):
                    self.text_to_speech(word, language, filename)
                
                self._loading_words.discard(cache_key)
            except:
                self._loading_words.discard(cache_key)
        
        thread = threading.Thread(target=_preload, daemon=True)
        thread.start()
    
    def get_word_audio_path(self, word, language='en'):
        if not word:
            return None
        
        word = word.strip()
        if not word:
            return None
        
        filename = f"{word.lower().replace(' ', '_')}_{language}.wav"
        file_path = os.path.join(self.audio_dir, filename)
        
        if not os.path.exists(file_path):
            self.text_to_speech(word, language, filename)
        
        return file_path if os.path.exists(file_path) else None
    
    def clean_temp_files(self):
        try:
            if not os.path.exists(self.audio_dir):
                return
            
            files = os.listdir(self.audio_dir)
            
            for file in files:
                if file.endswith('.tmp'):
                    try:
                        os.remove(os.path.join(self.audio_dir, file))
                    except:
                        pass
        except Exception as e:
            print(f"清理临时文件失败: {e}")
    
    def clear_cache(self):
        self._tts_cache.clear()
        self._loading_words.clear()

audio_manager = AudioManager()
