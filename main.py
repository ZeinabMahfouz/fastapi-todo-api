from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Task API")

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Complete FlyRank assignment", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": True}
]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="The title of the task cannot be empty")

@app.get("/")
def read_root():
    return {
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate):
    
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    
    new_task = {
        "id": new_id,
        "title": task_input.title.strip(),
        "done": False
    }
    
    if not new_task["title"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty or just spaces"
        )
        
    tasks.append(new_task)
    return new_task