from .database import DatabaseManager
from .word import Word
from datetime import datetime, timedelta

class LearningRecord:
    _review_cache = {}
    _cache_timestamp = None
    CACHE_DURATION = 30  # 缓存30秒
    
    def __init__(self, id=None, user_id=None, word_id=None, last_reviewed=None, 
                 next_review=None, review_count=0, difficulty=0.5, 
                 easiness_factor=2.5, interval=1):
        self.id = id
        self.user_id = user_id
        self.word_id = word_id
        self.last_reviewed = last_reviewed
        self.next_review = next_review
        self.review_count = review_count
        self.difficulty = difficulty
        self.easiness_factor = easiness_factor
        self.interval = interval
        self.db = DatabaseManager()
    
    def save(self):
        """保存学习记录到数据库"""
        try:
            if self.id is None:
                query = '''
                INSERT INTO learning_records (user_id, word_id, last_reviewed, next_review,
                                             review_count, difficulty, easiness_factor, interval)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (self.user_id, self.word_id, self.last_reviewed, self.next_review,
                          self.review_count, self.difficulty, self.easiness_factor, self.interval)
                cursor = self.db.execute_query(query, params)
                self.id = cursor.lastrowid
            else:
                query = '''
                UPDATE learning_records SET last_reviewed = ?, next_review = ?, review_count = ?,
                                           difficulty = ?, easiness_factor = ?, interval = ?
                WHERE id = ?
                '''
                params = (self.last_reviewed, self.next_review, self.review_count,
                          self.difficulty, self.easiness_factor, self.interval, self.id)
                self.db.execute_query(query, params)
            
            return self.id
        except Exception as e:
            print(f"Error saving learning record: {e}")
            return None
    
    def update_after_review(self, quality):
        """
        根据复习质量更新学习记录
        quality: 回答质量 (0-5)
            0: 完全不知道
            1: 错误回答，但看到正确答案后想起来了
            2: 错误回答，但正确答案看起来很熟悉
            3: 正确回答，但费了很大劲
            4: 正确回答，有些犹豫
            5: 完美回答
        """
        try:
            # 更新复习次数
            self.review_count += 1
            
            # 更新最后复习时间
            self.last_reviewed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 更新难度因子 (SM-2算法)
            if quality < 3:  # 回答错误
                self.interval = 1
                self.difficulty = min(1.0, self.difficulty + (1 - quality) * 0.1)
            else:  # 回答正确
                # 更新难度
                self.difficulty = max(0.0, self.difficulty - (quality - 3) * 0.15)
                
                # 更新难度因子
                self.easiness_factor = self.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
                if self.easiness_factor < 1.3:
                    self.easiness_factor = 1.3
                
                # 计算下次复习间隔
                if self.review_count == 1:
                    self.interval = 1
                elif self.review_count == 2:
                    self.interval = 6
                else:
                    self.interval = int(round(self.interval * self.easiness_factor))
            
            # 计算下次复习时间
            self.next_review = (datetime.now() + timedelta(days=self.interval)).strftime("%Y-%m-%d %H:%M:%S")
            
            # 记录到复习历史
            self._record_review_history(quality)
            
            # 保存更新
            self.save()
        except Exception as e:
            print(f"Error in update_after_review: {e}")
    
    def _record_review_history(self, quality):
        """记录每日复习历史"""
        try:
            if not self.user_id:
                return
                
            db = DatabaseManager()
            today = datetime.now().strftime("%Y-%m-%d")
            
            query = "SELECT * FROM review_history WHERE user_id = ? AND date = ?"
            result = db.fetch_one(query, (self.user_id, today))
            
            if result:
                update_query = '''
                UPDATE review_history 
                SET reviewed_count = reviewed_count + 1,
                    total_reviews = total_reviews + 1,
                    avg_quality = (avg_quality * total_reviews + ?) / (total_reviews + 1)
                WHERE user_id = ? AND date = ?
                '''
                db.execute_query(update_query, (quality, self.user_id, today))
            else:
                insert_query = '''
                INSERT INTO review_history (user_id, date, reviewed_count, total_reviews, avg_quality)
                VALUES (?, ?, 1, 1, ?)
                '''
                db.execute_query(insert_query, (self.user_id, today, quality))
        except Exception as e:
            print(f"Error recording review history: {e}")
    
    @classmethod
    def get_by_id(cls, record_id):
        """根据ID获取学习记录"""
        db = DatabaseManager()
        
        query = "SELECT * FROM learning_records WHERE id = ?"
        result = db.fetch_one(query, (record_id,))
        
        if result:
            return cls(
                id=result['id'],
                user_id=result['user_id'],
                word_id=result['word_id'],
                last_reviewed=result['last_reviewed'],
                next_review=result['next_review'],
                review_count=result['review_count'],
                difficulty=result['difficulty'],
                easiness_factor=result['easiness_factor'],
                interval=result['interval']
            )
        return None
    
    @classmethod
    def get_by_user_and_word(cls, user_id, word_id):
        """根据用户ID和单词ID获取学习记录"""
        db = DatabaseManager()
        
        query = "SELECT * FROM learning_records WHERE user_id = ? AND word_id = ?"
        result = db.fetch_one(query, (user_id, word_id))
        
        if result:
            return cls(
                id=result['id'],
                user_id=result['user_id'],
                word_id=result['word_id'],
                last_reviewed=result['last_reviewed'],
                next_review=result['next_review'],
                review_count=result['review_count'],
                difficulty=result['difficulty'],
                easiness_factor=result['easiness_factor'],
                interval=result['interval']
            )
        return None
    
    @classmethod
    def get_review_words(cls, user_id, limit=20):
        """获取需要复习的单词（带缓存）"""
        cache_key = f"{user_id}_{limit}"
        current_time = datetime.now()
        
        if cls._cache_timestamp and (current_time - cls._cache_timestamp).total_seconds() < cls.CACHE_DURATION:
            if cache_key in cls._review_cache:
                return cls._review_cache[cache_key]
        
        db = DatabaseManager()
        
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        query = '''
        SELECT lr.*, w.* FROM learning_records lr
        JOIN words w ON lr.word_id = w.id
        WHERE lr.user_id = ? AND lr.next_review <= ?
        ORDER BY lr.next_review ASC
        LIMIT ?
        '''
        results = db.fetch_all(query, (user_id, current_time_str, limit))
        
        review_items = []
        for result in results:
            word = Word(
                id=result['word_id'],
                word=result['word'],
                translation=result['translation'],
                definition=result['definition'],
                example=result['example'],
                phonetic=result['phonetic'],
                audio_path=result['audio_path'],
                image_path=result['image_path'],
                dictionary_id=result['dictionary_id']
            )
            
            record = cls(
                id=result['id'],
                user_id=result['user_id'],
                word_id=result['word_id'],
                last_reviewed=result['last_reviewed'],
                next_review=result['next_review'],
                review_count=result['review_count'],
                difficulty=result['difficulty'],
                easiness_factor=result['easiness_factor'],
                interval=result['interval']
            )
            
            review_items.append((word, record))
        
        cls._review_cache[cache_key] = review_items
        cls._cache_timestamp = datetime.now()
        
        return review_items
    
    @classmethod
    def clear_cache(cls):
        """清除复习缓存"""
        cls._review_cache.clear()
        cls._cache_timestamp = None
    
    @classmethod
    def get_review_count(cls, user_id):
        """获取今日需要复习的单词数量"""
        db = DatabaseManager()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = '''
        SELECT COUNT(*) as count FROM learning_records
        WHERE user_id = ? AND next_review <= ?
        '''
        result = db.fetch_one(query, (user_id, current_time))
        
        return result['count'] if result else 0
    
    @classmethod
    def get_learning_stats(cls, user_id, dictionary_id=None):
        """获取学习统计信息"""
        db = DatabaseManager()
        
        query = '''
        SELECT COUNT(*) as total,
               SUM(CASE WHEN review_count > 0 THEN 1 ELSE 0 END) as learned,
               SUM(CASE WHEN next_review <= ? THEN 1 ELSE 0 END) as need_review
        FROM learning_records lr
        JOIN words w ON lr.word_id = w.id
        WHERE lr.user_id = ?
        '''
        params = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id]
        
        if dictionary_id:
            query += " AND w.dictionary_id = ?"
            params.append(dictionary_id)
        
        result = db.fetch_one(query, params)
        
        return {
            'total': int(result['total']) if result and result['total'] else 0,
            'learned': int(result['learned']) if result and result['learned'] else 0,
            'need_review': int(result['need_review']) if result and result['need_review'] else 0
        }
    
    @classmethod
    def create_initial_records(cls, user_id, dictionary_id):
        """为词库中的所有单词创建初始学习记录"""
        db = DatabaseManager()
        
        query = "SELECT id FROM words WHERE dictionary_id = ?"
        word_results = db.fetch_all(query, (dictionary_id,))
        
        for word_result in word_results:
            word_id = word_result['id']
            
            check_query = "SELECT id FROM learning_records WHERE user_id = ? AND word_id = ?"
            existing = db.fetch_one(check_query, (user_id, word_id))
            
            if not existing:
                insert_query = '''
                INSERT INTO learning_records (user_id, word_id, last_reviewed, next_review,
                                             review_count, difficulty, easiness_factor, interval)
                VALUES (?, ?, NULL, ?, 0, 0.5, 2.5, 1)
                '''
                next_review = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.execute_query(insert_query, (user_id, word_id, next_review))
        
        return len(word_results)
    
    @classmethod
    def get_review_history(cls, user_id, days=7):
        """获取最近N天的复习历史数据"""
        try:
            db = DatabaseManager()
            
            # 计算开始日期
            from datetime import datetime, timedelta
            start_date = (datetime.now() - timedelta(days=days-1)).strftime("%Y-%m-%d")
            
            query = '''
            SELECT date, reviewed_count, avg_quality 
            FROM review_history 
            WHERE user_id = ? AND date >= ?
            ORDER BY date ASC
            '''
            results = db.fetch_all(query, (user_id, start_date))
            
            history = []
            for result in results:
                history.append({
                    'date': result['date'],
                    'reviewed_count': result['reviewed_count'],
                    'avg_quality': result['avg_quality']
                })
            
            return history
        except Exception as e:
            print(f"Error getting review history: {e}")
            return []
    
    @classmethod
    def get_review_stats(cls, user_id):
        """获取复习统计数据"""
        try:
            db = DatabaseManager()
            
            # 获取今日复习数据
            today = datetime.now().strftime("%Y-%m-%d")
            today_query = "SELECT * FROM review_history WHERE user_id = ? AND date = ?"
            today_result = db.fetch_one(today_query, (user_id, today))
            
            # 获取总复习次数
            total_query = "SELECT SUM(reviewed_count) as total FROM review_history WHERE user_id = ?"
            total_result = db.fetch_one(total_query, (user_id,))
            
            # 获取最近7天数据
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            week_query = "SELECT SUM(reviewed_count) as weekly, AVG(avg_quality) as avg_q FROM review_history WHERE user_id = ? AND date >= ?"
            week_result = db.fetch_one(week_query, (user_id, week_ago))
            
            return {
                'today_reviewed': int(today_result['reviewed_count']) if today_result and today_result['reviewed_count'] is not None else 0,
                'today_avg_quality': float(today_result['avg_quality']) if today_result and today_result['avg_quality'] is not None else 0.0,
                'total_reviewed': int(total_result['total']) if total_result and total_result['total'] else 0,
                'weekly_reviewed': int(week_result['weekly']) if week_result and week_result['weekly'] else 0,
                'weekly_avg_quality': float(week_result['avg_q']) if week_result and week_result['avg_q'] else 0.0
            }
        except Exception as e:
            print(f"Error getting review stats: {e}")
            return {
                'today_reviewed': 0,
                'today_avg_quality': 0,
                'total_reviewed': 0,
                'weekly_reviewed': 0,
                'weekly_avg_quality': 0
            }

    @classmethod
    def record_learning_time(cls, user_id, duration_seconds, time_type='review'):
        """记录学习时长
        time_type: 'review' 或 'test'
        """
        try:
            db = DatabaseManager()
            today = datetime.now().strftime("%Y-%m-%d")
            
            query = "SELECT * FROM learning_time WHERE user_id = ? AND date = ?"
            result = db.fetch_one(query, (user_id, today))
            
            if result:
                if time_type == 'review':
                    update_query = '''
                    UPDATE learning_time 
                    SET review_time = review_time + ?,
                        total_time = total_time + ?
                    WHERE user_id = ? AND date = ?
                    '''
                    db.execute_query(update_query, (duration_seconds, duration_seconds, user_id, today))
                else:
                    update_query = '''
                    UPDATE learning_time 
                    SET test_time = test_time + ?,
                        total_time = total_time + ?
                    WHERE user_id = ? AND date = ?
                    '''
                    db.execute_query(update_query, (duration_seconds, duration_seconds, user_id, today))
            else:
                if time_type == 'review':
                    insert_query = '''
                    INSERT INTO learning_time (user_id, date, review_time, test_time, total_time)
                    VALUES (?, ?, ?, 0, ?)
                    '''
                    db.execute_query(insert_query, (user_id, today, duration_seconds, duration_seconds))
                else:
                    insert_query = '''
                    INSERT INTO learning_time (user_id, date, review_time, test_time, total_time)
                    VALUES (?, ?, 0, ?, ?)
                    '''
                    db.execute_query(insert_query, (user_id, today, duration_seconds, duration_seconds))
        except Exception as e:
            print(f"Error recording learning time: {e}")

    @classmethod
    def get_learning_time_stats(cls, user_id, days=7):
        """获取学习时间统计"""
        try:
            db = DatabaseManager()
            start_date = (datetime.now() - timedelta(days=days-1)).strftime("%Y-%m-%d")
            
            query = '''
            SELECT date, review_time, test_time, total_time
            FROM learning_time
            WHERE user_id = ? AND date >= ?
            ORDER BY date ASC
            '''
            results = db.fetch_all(query, (user_id, start_date))
            
            stats = []
            for result in results:
                stats.append({
                    'date': result['date'],
                    'review_time': result['review_time'],
                    'test_time': result['test_time'],
                    'total_time': result['total_time']
                })
            
            return stats
        except Exception as e:
            print(f"Error getting learning time stats: {e}")
            return []

    @classmethod
    def get_today_learning_time(cls, user_id):
        """获取今日学习时间"""
        try:
            db = DatabaseManager()
            today = datetime.now().strftime("%Y-%m-%d")
            
            query = "SELECT * FROM learning_time WHERE user_id = ? AND date = ?"
            result = db.fetch_one(query, (user_id, today))
            
            if result:
                return {
                    'review_time': result['review_time'],
                    'test_time': result['test_time'],
                    'total_time': result['total_time']
                }
            return {'review_time': 0, 'test_time': 0, 'total_time': 0}
        except Exception as e:
            print(f"Error getting today learning time: {e}")
            return {'review_time': 0, 'test_time': 0, 'total_time': 0}

    @classmethod
    def get_weekly_learning_time(cls, user_id):
        """获取本周学习时间统计"""
        try:
            stats = cls.get_learning_time_stats(user_id, 7)
            weekly_stats = {str((datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")): 0 for i in range(6, -1, -1)}
            
            for stat in stats:
                date_key = stat['date']
                if date_key in weekly_stats:
                    weekly_stats[date_key] = stat['total_time']
            
            return weekly_stats
        except Exception as e:
            print(f"Error getting weekly learning time: {e}")
            return {}

    @classmethod
    def record_test_result(cls, user_id, dictionary_id, test_type, total_questions, correct_answers):
        """记录测试结果"""
        try:
            db = DatabaseManager()
            
            score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            
            query = '''
            INSERT INTO test_records (user_id, dictionary_id, test_type, total_questions, correct_answers, score)
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            db.execute_query(query, (user_id, dictionary_id, test_type, total_questions, correct_answers, score))
        except Exception as e:
            print(f"Error recording test result: {e}")

    @classmethod
    def get_test_stats(cls, user_id):
        """获取测试统计数据"""
        try:
            db = DatabaseManager()
            
            today = datetime.now().strftime("%Y-%m-%d")
            today_start = today + " 00:00:00"
            today_end = today + " 23:59:59"
            
            today_query = '''
            SELECT COUNT(*) as test_count, AVG(score) as avg_score, SUM(correct_answers) as correct, SUM(total_questions) as total
            FROM test_records 
            WHERE user_id = ? AND test_date BETWEEN ? AND ?
            '''
            today_result = db.fetch_one(today_query, (user_id, today_start, today_end))
            
            total_query = '''
            SELECT COUNT(*) as test_count, AVG(score) as avg_score, SUM(correct_answers) as correct, SUM(total_questions) as total
            FROM test_records 
            WHERE user_id = ?
            '''
            total_result = db.fetch_one(total_query, (user_id,))
            
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            week_query = '''
            SELECT COUNT(*) as test_count, AVG(score) as avg_score
            FROM test_records 
            WHERE user_id = ? AND test_date >= ?
            '''
            week_result = db.fetch_one(week_query, (user_id, week_ago))
            
            return {
                'today_tests': int(today_result['test_count']) if today_result and today_result['test_count'] else 0,
                'today_avg_score': float(today_result['avg_score']) if today_result and today_result['avg_score'] else 0.0,
                'today_correct': int(today_result['correct']) if today_result and today_result['correct'] else 0,
                'today_total': int(today_result['total']) if today_result and today_result['total'] else 0,
                'total_tests': int(total_result['test_count']) if total_result and total_result['test_count'] else 0,
                'total_avg_score': float(total_result['avg_score']) if total_result and total_result['avg_score'] else 0.0,
                'weekly_tests': int(week_result['test_count']) if week_result and week_result['test_count'] else 0,
                'weekly_avg_score': float(week_result['avg_score']) if week_result and week_result['avg_score'] else 0.0
            }
        except Exception as e:
            print(f"Error getting test stats: {e}")
            return {
                'today_tests': 0, 'today_avg_score': 0, 'today_correct': 0, 'today_total': 0,
                'total_tests': 0, 'total_avg_score': 0, 'weekly_tests': 0, 'weekly_avg_score': 0
            }