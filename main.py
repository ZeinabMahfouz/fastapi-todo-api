from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Task API")

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Complete FlyRank assignment", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": True}
]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="The title of the task cannot be empty")

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

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

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_input: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if task_input.title is not None:
                cleaned_title = task_input.title.strip()
                if not cleaned_title:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Title cannot be empty"
                    )
                task["title"] = cleaned_title
            
            if task_input.done is not None:
                task["done"] = task_input.done
                
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {task_id} not found"
    )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {task_id} not found"
    )