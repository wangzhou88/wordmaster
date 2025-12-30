from .database import db_manager

_word_cache = {}
_dictionary_word_count_cache = {}
CACHE_EXPIRY = 120

def _is_cache_valid(cache_time):
    """检查缓存是否有效"""
    from datetime import datetime
    if cache_time is None:
        return False
    return (datetime.now() - cache_time).total_seconds() < CACHE_EXPIRY

class Word:
    def __init__(self, id=None, word=None, translation=None, definition=None, 
                 example=None, phonetic=None, audio_path=None, image_path=None, 
                 dictionary_id=None):
        self.id = id
        self.word = word
        self.translation = translation
        self.definition = definition
        self.example = example
        self.phonetic = phonetic
        self.audio_path = audio_path
        self.image_path = image_path
        self.dictionary_id = dictionary_id
    
    def save(self):
        """保存单词到数据库"""
        global db_manager, _word_cache
        
        if self.id is not None and self.id in _word_cache:
            del _word_cache[self.id]
        
        if self.id is None:
            query = '''
            INSERT INTO words (word, translation, definition, example, phonetic, 
                              audio_path, image_path, dictionary_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (self.word, self.translation, self.definition, self.example,
                      self.phonetic, self.audio_path, self.image_path, self.dictionary_id)
            cursor = db_manager.execute_query(query, params)
            self.id = cursor.lastrowid
            
            _dictionary_word_count_cache[self.dictionary_id] = None
            
            db_manager.execute_query(
                "UPDATE dictionaries SET word_count = word_count + 1 WHERE id = ?",
                (self.dictionary_id,),
                use_cache=False
            )
        else:
            query = '''
            UPDATE words SET word = ?, translation = ?, definition = ?, example = ?,
                           phonetic = ?, audio_path = ?, image_path = ?, dictionary_id = ?
            WHERE id = ?
            '''
            params = (self.word, self.translation, self.definition, self.example,
                      self.phonetic, self.audio_path, self.image_path, self.dictionary_id,
                      self.id)
            db_manager.execute_query(query, params, use_cache=False)
        
        return self.id
    
    def delete(self):
        """从数据库删除单词"""
        global db_manager, _word_cache, _dictionary_word_count_cache
        
        if self.id is not None:
            if self.id in _word_cache:
                del _word_cache[self.id]
            
            _dictionary_word_count_cache[self.dictionary_id] = None
            
            db_manager.execute_query(
                "DELETE FROM learning_records WHERE word_id = ?",
                (self.id,),
                use_cache=False
            )
            
            db_manager.execute_query(
                "DELETE FROM words WHERE id = ?",
                (self.id,),
                use_cache=False
            )
            
            db_manager.execute_query(
                "UPDATE dictionaries SET word_count = word_count - 1 WHERE id = ?",
                (self.dictionary_id,),
                use_cache=False
            )
            
            return True
        return False
    
    @classmethod
    def get_by_id(cls, word_id):
        """根据ID获取单词"""
        global db_manager, _word_cache
        from datetime import datetime
        
        if word_id in _word_cache:
            cached = _word_cache[word_id]
            if _is_cache_valid(cached.get('time')):
                return cached.get('word')
        
        query = "SELECT * FROM words WHERE id = ?"
        result = db_manager.fetch_one(query, (word_id,))
        
        if result:
            word = cls(
                id=result['id'],
                word=result['word'],
                translation=result['translation'],
                definition=result['definition'],
                example=result['example'],
                phonetic=result['phonetic'],
                audio_path=result['audio_path'],
                image_path=result['image_path'],
                dictionary_id=result['dictionary_id']
            )
            _word_cache[word_id] = {
                'word': word,
                'time': datetime.now()
            }
            return word
        return None
    
    @classmethod
    def get_by_dictionary(cls, dictionary_id, limit=None, offset=0, use_cache=True):
        """获取词库中的单词"""
        global db_manager
        from datetime import datetime
        
        if use_cache and limit is None and offset == 0:
            cache_key = f"dict_{dictionary_id}"
            if cache_key in _word_cache:
                cached = _word_cache[cache_key]
                if _is_cache_valid(cached.get('time')):
                    return cached.get('words', [])
        
        query = "SELECT * FROM words WHERE dictionary_id = ?"
        params = [dictionary_id]
        
        if limit:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        results = db_manager.fetch_all(query, params, use_cache=use_cache)
        
        words = []
        for result in results:
            words.append(cls(
                id=result['id'],
                word=result['word'],
                translation=result['translation'],
                definition=result['definition'],
                example=result['example'],
                phonetic=result['phonetic'],
                audio_path=result['audio_path'],
                image_path=result['image_path'],
                dictionary_id=result['dictionary_id']
            ))
        
        if use_cache and limit is None and offset == 0:
            _word_cache[cache_key] = {
                'words': words,
                'time': datetime.now()
            }
        
        return words
    
    @classmethod
    def search(cls, keyword, dictionary_id=None, limit=20):
        """搜索单词"""
        global db_manager
        
        query = "SELECT * FROM words WHERE word LIKE ? OR translation LIKE ?"
        params = [f"%{keyword}%", f"%{keyword}%"]
        
        if dictionary_id:
            query += " AND dictionary_id = ?"
            params.append(dictionary_id)
        
        query += " LIMIT ?"
        params.append(limit)
        
        results = db_manager.fetch_all(query, params)
        
        words = []
        for result in results:
            words.append(cls(
                id=result['id'],
                word=result['word'],
                translation=result['translation'],
                definition=result['definition'],
                example=result['example'],
                phonetic=result['phonetic'],
                audio_path=result['audio_path'],
                image_path=result['image_path'],
                dictionary_id=result['dictionary_id']
            ))
        
        return words
    
    @classmethod
    def count_by_dictionary(cls, dictionary_id):
        """统计词库中的单词数量"""
        global db_manager, _dictionary_word_count_cache
        from datetime import datetime
        
        if dictionary_id in _dictionary_word_count_cache:
            cached = _dictionary_word_count_cache[dictionary_id]
            if _is_cache_valid(cached.get('time')):
                return cached.get('count')
        
        query = "SELECT COUNT(*) as count FROM words WHERE dictionary_id = ?"
        result = db_manager.fetch_one(query, (dictionary_id,))
        
        count = result['count'] if result else 0
        
        _dictionary_word_count_cache[dictionary_id] = {
            'count': count,
            'time': datetime.now()
        }
        
        return count
    
    @classmethod
    def clear_cache(cls):
        """清除所有缓存"""
        global _word_cache, _dictionary_word_count_cache
        _word_cache.clear()
        _dictionary_word_count_cache.clear()