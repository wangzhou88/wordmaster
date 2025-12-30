from .database import DatabaseManager
import json

_word_cache = {}
CACHE_EXPIRY = 120

def _is_cache_valid(cache_time):
    """检查缓存是否有效"""
    from datetime import datetime
    if cache_time is None:
        return False
    return (datetime.now() - cache_time).total_seconds() < CACHE_EXPIRY

class User:
    def __init__(self, id=None, name=None, settings=None):
        self.id = id
        self.name = name
        self.settings = settings if settings else self._get_default_settings()
        self.db = DatabaseManager()
    
    def _get_default_settings(self):
        """获取默认设置"""
        return {
            'language': 'zh',
            'auto_play_audio': True,
            'daily_target': 20,
            'review_reminder': True,
            'theme': 'light'
        }
    
    def save(self):
        """保存用户到数据库"""
        settings_json = json.dumps(self.settings)
        
        if self.id is None:
            query = '''
            INSERT INTO users (name, settings)
            VALUES (?, ?)
            '''
            params = (self.name, settings_json)
            cursor = self.db.execute_query(query, params)
            self.id = cursor.lastrowid
        else:
            query = '''
            UPDATE users SET name = ?, settings = ?
            WHERE id = ?
            '''
            params = (self.name, settings_json, self.id)
            self.db.execute_query(query, params)
        
        global _word_cache
        _word_cache.clear()
        
        return self.id
    
    def delete(self):
        """从数据库删除用户"""
        if self.id is not None:
            self.db.execute_query(
                "DELETE FROM learning_records WHERE user_id = ?",
                (self.id,)
            )
            
            self.db.execute_query(
                "DELETE FROM test_records WHERE user_id = ?",
                (self.id,)
            )
            
            self.db.execute_query(
                "DELETE FROM users WHERE id = ?",
                (self.id,)
            )
            
            global _word_cache
            _word_cache.clear()
            
            return True
        return False
    
    def update_settings(self, new_settings):
        """更新用户设置"""
        self.settings.update(new_settings)
        self.save()
    
    @classmethod
    def get_by_id(cls, user_id):
        """根据ID获取用户"""
        global _word_cache
        from datetime import datetime
        
        if user_id in _word_cache:
            cached = _word_cache[user_id]
            if _is_cache_valid(cached.get('time')):
                return cached.get('user')
        
        query = "SELECT * FROM users WHERE id = ?"
        result = DatabaseManager().fetch_one(query, (user_id,))
        
        if result:
            settings = json.loads(result['settings']) if result['settings'] else cls._get_default_settings(cls)
            user = cls(
                id=result['id'],
                name=result['name'],
                settings=settings
            )
            _word_cache[user_id] = {
                'user': user,
                'time': datetime.now()
            }
            return user
        return None
    
    @classmethod
    def get_all(cls):
        """获取所有用户"""
        query = "SELECT * FROM users ORDER BY created_at DESC"
        results = DatabaseManager().fetch_all(query)
        
        users = []
        for result in results:
            settings = json.loads(result['settings']) if result['settings'] else cls._get_default_settings(cls)
            users.append(cls(
                id=result['id'],
                name=result['name'],
                settings=settings
            ))
        
        return users
    
    @classmethod
    def create_default_user(cls):
        """创建默认用户"""
        users = cls.get_all()
        if users:
            return users[0]
        
        default_user = cls(name="默认用户")
        default_user.save()
        return default_user
