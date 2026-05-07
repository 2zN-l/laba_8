import sqlite3
import os

class StatsDatabase:
    def __init__(self, db_path="snake_stats.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS games (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        score INTEGER,
                        duration_seconds REAL
                    )
                """)
                conn.commit()
                print(f"База данных подключена: {self.db_path}")
        except Exception as e:
            print(f"Ошибка БД: {e}")

    def save_game(self, score: int, duration: float):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO games (score, duration_seconds) VALUES (?, ?)", (score, duration))
                conn.commit()
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def get_top_scores(self, limit: int = 10):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT played_at, score, duration_seconds FROM games ORDER BY score DESC LIMIT ?", (limit,))
                return cursor.fetchall()
        except:
            return []

    def get_stats(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*), AVG(score), MAX(score) FROM games")
                row = cursor.fetchone()
                return {"total": row[0] or 0, "avg": round(row[1] or 0, 2), "max": row[2] or 0}
        except:
            return {"total": 0, "avg": 0, "max": 0}