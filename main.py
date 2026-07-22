import sqlite3
from fastapi import FastAPI, HTTPException, status
from models import TaskCreate, TaskUpdate

app = FastAPI(title="Task API with SQLite")

DB_NAME = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # لإرجاع النتائج كـ Dictionaries سهلة الاستخدام مع FastAPI
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    
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

# 1. جلب كل المهام من قاعدة البيانات
@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    # تحويل نتائج قاعدة البيانات إلى مصفوفة قواميس (List of Dicts)
    tasks_list = [dict(row) for row in rows]
    # تحويل قيمة done من 0/1 إلى True/False
    for task in tasks_list:
        task["done"] = bool(task["done"])
        
    return tasks_list

# 2. جلب مهمة واحدة بواسطة الـ ID مع استعلام معالج (Parameterized Query)
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task {task_id} not found"
        )
        
    task = dict(row)
    task["done"] = bool(task["done"])
    return task