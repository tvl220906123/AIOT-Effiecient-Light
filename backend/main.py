from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from routes import translate  
from Notify import start_scheduler, send_daily_notification
from routes.task_db import add_task, get_tasks

app = FastAPI()

start_scheduler()

@app.post("/add-task")
def create_task(task: dict):
    add_task(task['name'], task['deadline'])
    return {"message": "Task added"}

@app.get("/tasks")
def list_tasks():
    return get_tasks()

class TaskInput(BaseModel):
    name: str
    deadline: str
    created_at: str

@app.post("/predict-risk")
def predict_risk(task: TaskInput):
    deadline = datetime.fromisoformat(task.deadline)
    created = datetime.fromisoformat(task.created_at)
    now = datetime.now()

    days_left = (deadline - now).days
    days_total = (deadline - created).days

    if days_left <= 3 and days_total >= 10:
        risk = "HIGH"
    elif days_left <= 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "task": task.name,
        "days_left": days_left,
        "risk_level": risk
    }

@app.get("/notify")
def trigger_notification():
    send_daily_notification()
    return {"message": "Notification sent"}

app.include_router(translate.router)



