"""Tkinter view of the shared task manager."""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from backend import TaskStore


class TaskWindow:
    def __init__(self, root, store):
        self.root, self.store = root, store
        root.title('Lab 4 | Task Manager | Tkinter')
        root.geometry('720x460')
        root.minsize(540, 350)
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='My tasks', font=('Helvetica', 24, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='Tkinter interface • Shared local task database').pack(anchor='w', pady=(2, 16))
        entry_row = ttk.Frame(frame)
        entry_row.pack(fill='x')
        self.title = tk.StringVar()
        self.entry = ttk.Entry(entry_row, textvariable=self.title)
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
        self.entry.bind('<Return>', lambda event: self.add())
        ttk.Button(entry_row, text='Add task', command=self.add).pack(side='right')
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill='both', expand=True, pady=16)
        self.table = ttk.Treeview(table_frame, columns=('title', 'status'), show='headings', selectmode='browse')
        self.table.heading('title', text='Task')
        self.table.heading('status', text='Status')
        self.table.column('title', width=420)
        self.table.column('status', width=110, stretch=False)
        scroll = ttk.Scrollbar(table_frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        self.table.pack(fill='both', expand=True)
        actions = ttk.Frame(frame)
        actions.pack(fill='x')
        ttk.Button(actions, text='Toggle complete', command=lambda: self.change('toggle')).pack(side='left')
        ttk.Button(actions, text='Delete', command=lambda: self.change('delete')).pack(side='left', padx=8)
        ttk.Button(actions, text='Refresh', command=self.refresh).pack(side='right')
        self.status = tk.StringVar()
        ttk.Label(frame, textvariable=self.status).pack(anchor='w', pady=(12, 0))
        self.refresh()
        self.entry.focus_set()

    def refresh(self):
        try:
            rows = self.store.list_tasks()
        except sqlite3.Error as error:
            messagebox.showerror('Storage error', str(error), parent=self.root)
            return
        for item in self.table.get_children():
            self.table.delete(item)
        for task_id, title, done in rows:
            self.table.insert('', 'end', iid=str(task_id), values=(title, 'Complete' if done else 'To do'))
        self.status.set(f'{len(rows)} tasks • {sum(row[2] for row in rows)} complete')

    def add(self):
        try:
            self.store.add(self.title.get())
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror('Cannot add task', str(error), parent=self.root)
            return
        self.title.set('')
        self.refresh()

    def change(self, action):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo('Select a task', 'Select a task first.', parent=self.root)
            return
        if action == 'delete' and not messagebox.askyesno('Delete task', 'Delete the selected task?', parent=self.root):
            return
        try:
            getattr(self.store, action)(int(selected[0]))
        except sqlite3.Error as error:
            messagebox.showerror('Storage error', str(error), parent=self.root)
        self.refresh()


def run(path):
    root = tk.Tk()
    TaskWindow(root, TaskStore(path))
    root.mainloop()
