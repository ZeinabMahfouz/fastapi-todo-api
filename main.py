import sqlite3
from fastapi import FastAPI, HTTPException, status
from models import TaskCreate, TaskUpdate

app = FastAPI(title="Task API with SQLite")

DB_NAME = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
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

@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    tasks_list = [dict(row) for row in rows]
    for task in tasks_list:
        task["done"] = bool(task["done"])
    return tasks_list

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

# 1. إضافة مهمة جديدة إلى قاعدة البيانات (INSERT INTO)
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate):
    title = task_input.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # تنفيذ أمر الإضافة مع إبقاء done مساوياً لـ 0 (False) افتراضياً
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, 0))
    conn.commit()
    
    # جلب الـ ID الذي أنشأته قاعدة البيانات تلقائياً
    new_id = cursor.lastrowid
    conn.close()
    
    return {
        "id": new_id,
        "title": title,
        "done": False
    }