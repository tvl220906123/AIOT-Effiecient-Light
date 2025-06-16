from datetime import datetime
from routes.task_db import get_tasks
from apscheduler.schedulers.background import BackgroundScheduler

def send_daily_notification():
    tasks = get_tasks()
    today = datetime.today()

    for task in tasks:
        deadline = datetime.fromisoformat(task['deadline'])
        days_left = (deadline.date() - today.date()).days

        if 0 <= days_left <= 3:
            print(f"[ALERT] Task '{task['name']}' is due in {days_left} day(s) on {task['deadline']}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_notification, 'interval', hours=24)  # or use 'cron' for specific time
    scheduler.start()