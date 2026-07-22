import os
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, status, Response
from dotenv import load_dotenv
from models import TaskCreate, TaskUpdate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:dev@localhost:5432/tasks")

app = FastAPI(title="Task API with PostgreSQL")

def get_db_connection():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    return conn

def init_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            );
        """)
        
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        count = cursor.fetchone()["count"]
        
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

# 1. عرض جميع المهام (GET /tasks)
@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
        tasks = cursor.fetchall()
    conn.close()
    return tasks

# 2. عرض مهمة معينة حسب ID (GET /tasks/{id})
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
        task = cursor.fetchone()
    conn.close()
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )
    return task

# 3. إنشاء مهمة جديدة (POST /tasks)
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate):
    title = task_input.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )
        
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
            (title, False)
        )
        new_task = cursor.fetchone()
        conn.commit()
    conn.close()
    return new_task

# 4. تحديث مهمة (PUT /tasks/{id})
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_input: TaskUpdate):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
        existing_task = cursor.fetchone()
        
        if existing_task is None:
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
            
        new_title = existing_task["title"]
        if task_input.title is not None:
            cleaned_title = task_input.title.strip()
            if not cleaned_title:
                conn.close()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title cannot be empty"
                )
            new_title = cleaned_title
            
        new_done = task_input.done if task_input.done is not None else existing_task["done"]
        
        cursor.execute(
            "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
            (new_title, new_done, task_id)
        )
        updated_task = cursor.fetchone()
        conn.commit()
    conn.close()
    return updated_task

# 5. حذف مهمة (DELETE /tasks/{id})
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM tasks WHERE id = %s;", (task_id,))
        if cursor.fetchone() is None:
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
            
        cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
        conn.commit()
    conn.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)