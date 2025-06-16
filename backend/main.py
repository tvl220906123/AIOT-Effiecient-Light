from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from routes import translate
from Notify import start_scheduler, send_daily_notification
from routes.task_db import add_task, get_tasks
from fastapi.responses import JSONResponse

app = FastAPI()

start_scheduler()

# Models
class AddTaskInput(BaseModel):
    name: str
    deadline: str  # Expecting ISO format, e.g., "2025-06-20T12:00:00"

class TaskInput(BaseModel):
    name: str
    deadline: str
    created_at: str

class RiskResponse(BaseModel):
    task: str
    days_left: int
    risk_level: str

# Routes
@app.post("/add-task")
def create_task(task: AddTaskInput):
    try:
        datetime.fromisoformat(task.deadline)
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid deadline format. Use ISO format: YYYY-MM-DDTHH:MM:SS"})
    
    add_task(task.name, task.deadline)
    return {"message": "Task added"}

@app.get("/tasks")
def list_tasks():
    return get_tasks()

@app.post("/predict-risk", response_model=RiskResponse)
def predict_risk(task: TaskInput):
    try:
        deadline = datetime.fromisoformat(task.deadline)
        created = datetime.fromisoformat(task.created_at)
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM:SS"})

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
    """
    Trigger manual notification (e.g., for testing).
    Normally handled by scheduled job.
    """
    send_daily_notification()
    return {"message": "Notification sent"}

# Include additional routes
app.include_router(translate.router)