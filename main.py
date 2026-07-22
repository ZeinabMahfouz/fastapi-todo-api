import os
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, status, Response
from dotenv import load_dotenv
from models import TaskCreate, TaskUpdate

# تحميل المتغيرات البيئية من .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:dev@localhost:5432/tasks")

app = FastAPI(title="Task API with PostgreSQL")

def get_db_connection():
    # الاتصال بـ Postgres وتشكيل الصفوف على شكل Dictionaries
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    return conn

def init_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # 1. إنشاء جدول tasks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            );
        """)
        
        # 2. التحقق من وجود بيانات
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        count = cursor.fetchone()["count"]
        
        # 3. بذر البيانات لأول مرة فقط
        if count == 0:
            cursor.executemany("""
                INSERT INTO tasks (title, done) VALUES (%s, %s);
            """, [
                ("Buy milk", False),
                ("Complete FlyRank assignment", False),
                ("Learn FastAPI with PostgreSQL", True)
            ])
            conn.commit()
    conn.close()

init_db()

@app.get("/")
def read_root():
    return {
        "name": "Task API", 
        "version": "3.0", 
        "storage": "PostgreSQL Container",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}