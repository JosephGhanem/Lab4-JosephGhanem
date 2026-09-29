"""Shared SQLite storage used by both desktop interfaces."""
from pathlib import Path
import sqlite3

DEFAULT_DB = Path(__file__).resolve().parent / 'data' / 'tasks.sqlite3'


class TaskStore:
    def __init__(self, path=DEFAULT_DB):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS tasks '
                       '(id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)')

    def connect(self):
        return sqlite3.connect(self.path)

    def list_tasks(self):
        with self.connect() as db:
            return db.execute('SELECT id, title, done FROM tasks ORDER BY id').fetchall()

    def add(self, title):
        title = title.strip()
        if not title:
            raise ValueError('Enter a task title.')
        if len(title) > 200:
            raise ValueError('Keep task titles within 200 characters.')
        with self.connect() as db:
            return db.execute('INSERT INTO tasks (title) VALUES (?)', (title,)).lastrowid

    def toggle(self, task_id):
        with self.connect() as db:
            db.execute('UPDATE tasks SET done = 1 - done WHERE id = ?', (task_id,))

    def delete(self, task_id):
        with self.connect() as db:
            db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
