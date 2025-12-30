import sqlite3
import os
from datetime import datetime, timedelta
from functools import lru_cache

class DatabaseManager:
    _instance = None
    _connection = None
    _connection_time = None
    CONNECTION_MAX_AGE = 300  # 5分钟连接有效期
    _query_cache = {}
    _cache_max_size = 100
    
    def __new__(cls, db_path="wordmaster.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_path="wordmaster.db"):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), db_path)
        
    def _ensure_connection(self):
        """确保数据库连接有效"""
        current_time = datetime.now()
        if self._connection is None:
            self._connect()
        elif self._connection_time and (current_time - self._connection_time).total_seconds() > self.CONNECTION_MAX_AGE:
            self._close_connection()
            self._connect()
    
    def _connect(self):
        """建立数据库连接"""
        self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=NORMAL")
        self._connection.execute("PRAGMA cache_size=-64000")
        self._connection.execute("PRAGMA temp_store=MEMORY")
        self._connection.execute("PRAGMA mmap_size=268435456")
        self._connection_time = datetime.now()
        
    def _close_connection(self):
        """关闭数据库连接"""
        if self._connection:
            try:
                self._connection.close()
            except:
                pass
            self._connection = None
            self._connection_time = None
    
    def connect(self):
        """公共连接方法"""
        self._ensure_connection()
    
    def disconnect(self):
        """公共断开连接方法"""
        self._close_connection()
    
    def _get_cache_key(self, query, params):
        """生成缓存键"""
        return f"{query}:{str(params)}"
    
    def _get_cached_result(self, query, params):
        """获取缓存结果"""
        cache_key = self._get_cache_key(query, params)
        if cache_key in self._query_cache:
            cached = self._query_cache[cache_key]
            if (datetime.now() - cached['time']).total_seconds() < 60:
                return cached['result']
            else:
                del self._query_cache[cache_key]
        return None
    
    def _cache_result(self, query, params, result):
        """缓存查询结果"""
        cache_key = self._get_cache_key(query, params)
        if len(self._query_cache) >= self._cache_max_size:
            oldest_key = next(iter(self._query_cache))
            del self._query_cache[oldest_key]
        self._query_cache[cache_key] = {
            'result': result,
            'time': datetime.now()
        }
    
    def clear_cache(self):
        """清除查询缓存"""
        self._query_cache.clear()
    
    def execute_query(self, query, params=None, use_cache=True):
        """执行SQL查询"""
        if use_cache:
            cached = self._get_cached_result(query, params)
            if cached is not None:
                return cached
        
        self._ensure_connection()
        
        cursor = self._connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        self._connection.commit()
        
        return cursor
        
    def fetch_all(self, query, params=None, use_cache=True):
        """获取所有查询结果"""
        cursor = self.execute_query(query, params, use_cache)
        return cursor.fetchall()
        
    def fetch_one(self, query, params=None, use_cache=True):
        """获取单个查询结果"""
        cursor = self.execute_query(query, params, use_cache)
        return cursor.fetchone()
    
    def execute_many(self, query, params_list):
        """批量执行SQL"""
        self._ensure_connection()
        cursor = self._connection.cursor()
        cursor.executemany(query, params_list)
        self._connection.commit()
        return cursor
    
    def close(self):
        """关闭数据库连接"""
        self._close_connection()
    
    def create_tables(self):
        """创建数据库表"""
        self._connect()
        
        self._connection.execute('''
        CREATE TABLE IF NOT EXISTS dictionaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            language TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            word_count INTEGER DEFAULT 0
        )
        ''')
        
        self._connection.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            definition TEXT,
            example TEXT,
            phonetic TEXT,
            audio_path TEXT,
            image_path TEXT,
            dictionary_id INTEGER,
            FOREIGN KEY (dictionary_id) REFERENCES dictionaries(id)
        )
        ''')
        
        self._connection.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            settings TEXT
        )
        ''')
        
        self._connection.execute('''
        CREATE TABLE IF NOT EXISTS learning_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word_id INTEGER,
            last_reviewed TIMESTAMP,
            next_review TIMESTAMP,
            review_count INTEGER DEFAULT 0,
            difficulty FLOAT DEFAULT 0.5,
            easiness_factor FLOAT DEFAULT 2.5,
            interval INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (word_id) REFERENCES words(id)
        )
        ''')
        
        self._connection.execute('''
        CREATE TABLE IF NOT EXISTS test_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            dictionary_id INTEGER,
            test_type TEXT,
            total_questions INTEGER,
            correct_answers INTEGER,
            score FLOAT,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (dictionary_id) REFERENCES dictionaries(id)
        )
        ''')

        self._connection.execute('''
        CREATE TABLE IF NOT EXISTS review_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE,
            reviewed_count INTEGER DEFAULT 0,
            total_reviews INTEGER DEFAULT 0,
            avg_quality FLOAT DEFAULT 0,
            UNIQUE(user_id, date),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        self._connection.execute('''
        CREATE TABLE IF NOT EXISTS learning_time (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE,
            review_time INTEGER DEFAULT 0,
            test_time INTEGER DEFAULT 0,
            total_time INTEGER DEFAULT 0,
            UNIQUE(user_id, date),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_learning_time_user ON learning_time(user_id)")
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_learning_time_date ON learning_time(date)")
        
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_words_dictionary ON words(dictionary_id)")
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_words_word ON words(word)")
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_learning_records_word ON learning_records(word_id)")
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_learning_records_user ON learning_records(user_id)")
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_learning_records_user_review ON learning_records(user_id, next_review)")
        self._connection.execute("CREATE INDEX IF NOT EXISTS idx_learning_records_user_word ON learning_records(user_id, word_id)")
        
        self._connection.commit()
        self._close_connection()

db_manager = DatabaseManager()