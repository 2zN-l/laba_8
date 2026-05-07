import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from snake_game.db import StatsDatabase

app = FastAPI(title="Змейка - Статистика")

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "snake_stats.db")
db = StatsDatabase(db_path)

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Змейка - Статистика</title></head>
    <body style="font-family: Arial; text-align: center;">
        <h1>🐍 Статистика игр "Змейка"</h1>
        <ul style="list-style: none; padding: 0;">
            <li><a href="/games">📋 Список игр</a></li>
            <li><a href="/stats">📊 Общая статистика</a></li>
        </ul>
    </body>
    </html>
    """


@app.get("/games", response_class=HTMLResponse)
def games():
    games_data = db.get_top_scores(limit=20)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Список игр</title></head>
    <body style="font-family: Arial;">
        <h1>📋 Последние игры</h1>
        <table border="1" cellpadding="8" style="border-collapse: collapse;">
            <tr style="background: #333; color: white;">
                <th>Время</th><th>Счёт</th><th>Длительность (сек)</th>
            </tr>
    """
    
    for g in games_data:
        html += f"""
            <tr>
                <td>{g[0]}</td>
                <td style="text-align: center;"><b>{g[1]}</b></td>
                <td style="text-align: center;">{g[2]}</td>
            </tr>
        """
    
    html += """
        </table>
        <br>
        <a href="/">← На главную</a>
    </body>
    </html>
    """
    return html


@app.get("/stats", response_class=HTMLResponse)
def stats():
    stats_data = db.get_stats()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Статистика</title></head>
    <body style="font-family: Arial;">
        <h1>📊 Общая статистика</h1>
        <ul style="font-size: 18px;">
            <li>🎮 Всего игр: <b>{stats_data['total']}</b></li>
            <li>⭐ Средний счёт: <b>{stats_data['avg']}</b></li>
            <li>🏆 Рекорд: <b>{stats_data['max']}</b></li>
        </ul>
        <br>
        <a href="/">← На главную</a>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)