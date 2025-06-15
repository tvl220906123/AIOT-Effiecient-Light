from tinydb import TinyDB, Query

db = TinyDB('tasks.json')
Task = Query()

def add_task(name, deadline):
    db.insert({'name': name, 'deadline': deadline})

def get_tasks():
    return db.all()