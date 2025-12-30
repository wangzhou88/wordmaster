from .database import DatabaseManager
from .word import Word
import os
import json
import csv

class Dictionary:
    def __init__(self, id=None, name=None, description=None, language="en", word_count=0):
        self.id = id
        self.name = name
        self.description = description
        self.language = language
        self.word_count = word_count
        self.db = DatabaseManager()
    
    def save(self):
        """保存词库到数据库"""
        self.db.connect()
        
        if self.id is None:
            # 插入新词库
            query = '''
            INSERT INTO dictionaries (name, description, language)
            VALUES (?, ?, ?)
            '''
            params = (self.name, self.description, self.language)
            cursor = self.db.execute_query(query, params)
            self.id = cursor.lastrowid
        else:
            # 更新现有词库
            query = '''
            UPDATE dictionaries SET name = ?, description = ?, language = ?
            WHERE id = ?
            '''
            params = (self.name, self.description, self.language, self.id)
            self.db.execute_query(query, params)
        
        self.db.disconnect()
        return self.id
    
    def delete(self):
        """从数据库删除词库"""
        if self.id is not None:
            self.db.connect()
            
            # 获取词库中的所有单词
            words = Word.get_by_dictionary(self.id)
            
            # 删除每个单词的相关文件
            for word in words:
                if word.audio_path and os.path.exists(word.audio_path):
                    os.remove(word.audio_path)
                if word.image_path and os.path.exists(word.image_path):
                    os.remove(word.image_path)
                word.delete()
            
            # 删除词库
            self.db.execute_query(
                "DELETE FROM dictionaries WHERE id = ?",
                (self.id,)
            )
            
            self.db.disconnect()
            return True
        return False
    
    @classmethod
    def get_by_id(cls, dictionary_id):
        """根据ID获取词库"""
        db = DatabaseManager()
        db.connect()
        
        query = "SELECT * FROM dictionaries WHERE id = ?"
        result = db.fetch_one(query, (dictionary_id,))
        
        db.disconnect()
        
        if result:
            return cls(
                id=result['id'],
                name=result['name'],
                description=result['description'],
                language=result['language'],
                word_count=result['word_count']
            )
        return None
    
    @classmethod
    def get_all(cls):
        """获取所有词库"""
        db = DatabaseManager()
        db.connect()
        
        query = "SELECT * FROM dictionaries ORDER BY created_at DESC"
        results = db.fetch_all(query)
        
        db.disconnect()
        
        dictionaries = []
        for result in results:
            dictionaries.append(cls(
                id=result['id'],
                name=result['name'],
                description=result['description'],
                language=result['language'],
                word_count=result['word_count']
            ))
        
        return dictionaries
    
    def import_words(self, file_path):
        """从文件导入单词"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.txt':
            words = self._import_from_txt(file_path)
        elif file_ext == '.csv':
            words = self._import_from_csv(file_path)
        elif file_ext == '.json':
            words = self._import_from_json(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
        
        # 将单词添加到词库
        for word_data in words:
            word = Word(
                word=word_data.get('word'),
                translation=word_data.get('translation'),
                definition=word_data.get('definition'),
                example=word_data.get('example'),
                phonetic=word_data.get('phonetic'),
                dictionary_id=self.id
            )
            word.save()
        
        # 更新词库单词数量
        self.db.connect()
        self.db.execute_query(
            "UPDATE dictionaries SET word_count = (SELECT COUNT(*) FROM words WHERE dictionary_id = ?) WHERE id = ?",
            (self.id, self.id)
        )
        self.db.disconnect()
        
        return len(words)
    
    def export_words(self, file_path):
        """导出单词到文件"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 获取词库中的所有单词
        words = Word.get_by_dictionary(self.id)
        
        # 转换为字典列表
        words_data = []
        for word in words:
            words_data.append({
                'word': word.word,
                'translation': word.translation,
                'definition': word.definition,
                'example': word.example,
                'phonetic': word.phonetic
            })
        
        if file_ext == '.txt':
            self._export_to_txt(words_data, file_path)
        elif file_ext == '.csv':
            self._export_to_csv(words_data, file_path)
        elif file_ext == '.json':
            self._export_to_json(words_data, file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
        
        return len(words)
    
    def _import_from_txt(self, file_path):
        """从TXT文件导入单词"""
        words = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        word_data = {
                            'word': parts[0].strip(),
                            'translation': parts[1].strip()
                        }
                        if len(parts) > 2:
                            word_data['definition'] = parts[2].strip()
                        if len(parts) > 3:
                            word_data['example'] = parts[3].strip()
                        if len(parts) > 4:
                            word_data['phonetic'] = parts[4].strip()
                        words.append(word_data)
        return words
    
    def _import_from_csv(self, file_path):
        """从CSV文件导入单词"""
        words = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word_data = {
                    'word': row.get('word', '').strip(),
                    'translation': row.get('translation', '').strip(),
                    'definition': row.get('definition', '').strip(),
                    'example': row.get('example', '').strip(),
                    'phonetic': row.get('phonetic', '').strip()
                }
                if word_data['word'] and word_data['translation']:
                    words.append(word_data)
        return words
    
    def _import_from_json(self, file_path):
        """从JSON文件导入单词"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        words = []
        for item in data:
            word_data = {
                'word': item.get('word', '').strip(),
                'translation': item.get('translation', '').strip(),
                'definition': item.get('definition', '').strip(),
                'example': item.get('example', '').strip(),
                'phonetic': item.get('phonetic', '').strip()
            }
            if word_data['word'] and word_data['translation']:
                words.append(word_data)
        
        return words
    
    def _export_to_txt(self, words_data, file_path):
        """导出单词到TXT文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# 单词\t翻译\t释义\t例句\t音标\n")
            for word in words_data:
                line = f"{word['word']}\t{word['translation']}"
                if word.get('definition'):
                    line += f"\t{word['definition']}"
                if word.get('example'):
                    line += f"\t{word['example']}"
                if word.get('phonetic'):
                    line += f"\t{word['phonetic']}"
                f.write(line + '\n')
    
    def _export_to_csv(self, words_data, file_path):
        """导出单词到CSV文件"""
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['word', 'translation', 'definition', 'example', 'phonetic']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(words_data)
    
    def _export_to_json(self, words_data, file_path):
        """导出单词到JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(words_data, f, ensure_ascii=False, indent=2)