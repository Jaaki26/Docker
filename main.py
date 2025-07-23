from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
 
app = FastAPI()
DATA_FILE = "tasks.json"
 
class Task(BaseModel):
    id: int
    title: str
    done: bool = False
 
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)
 
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)
 
@app.get("/tasks")
def get_tasks():
    return load_tasks()
 
@app.post("/tasks")
def create_task(task: Task):
    tasks = load_tasks()
if any(t["id"] == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task ID already exists.")
    tasks.append(task.dict())
    save_tasks(tasks)
    return task
 
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks[i] = task.dict()
            save_tasks(tasks)
            return task
    raise HTTPException(status_code=404, detail="Task not found.")
 
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return {"message": "Task deleted."}
