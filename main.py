import sqlite3
from fastapi import FastAPI, HTTPException, status, Response
from models import TaskCreate, TaskUpdate

app = FastAPI(title="Task API with SQLite")

DB_NAME = "tasks.db"

def get_db_connection():
    """فتح اتصال بقاعدة البيانات وإرجاع الصفوف كقواميس Python"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """إنشاء الجدول والتعبئة الأولية عند بدء التطبيق"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. إنشاء جدول المهام إذا لم يكن موجوداً
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    
    # 2. التعبئة الأولية فقط إذا كان الجدول فارغاً
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    if count == 0:
        cursor.executemany("""
            INSERT INTO tasks (title, done) VALUES (?, ?)
        """, [
            ("Buy milk", 0),
            ("Complete FlyRank assignment", 0),
            ("Learn FastAPI with SQLite", 1)
        ])
    
    conn.commit()
    conn.close()

# تشغيل تهيئة قاعدة البيانات فور بدء التطبيق
init_db()

@app.get("/")
def read_root():
    return {
        "name": "Task API", 
        "version": "2.0", 
        "storage": "SQLite database",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}