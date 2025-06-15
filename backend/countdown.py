from datetime import datetime

def get_countdown(deadline: str) -> dict:
    deadline_dt = datetime.fromisoformat(deadline)
    now = datetime.now()
    delta = deadline_dt - now

    return {
        "days": delta.days,
        "hours": delta.seconds // 3600,
        "minutes": (delta.seconds % 3600) // 60,
        "seconds": delta.seconds % 60
    }