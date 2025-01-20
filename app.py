import os
import tkinter as tk
from tkinter import messagebox
import sqlite3


if os.path.exists("todo.db"):
    os.remove("todo.db")


def create_table():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()


def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, 'Pending'))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END) 
        load_tasks()  
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")


def mark_done(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    load_tasks() 


def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    load_tasks() 


def load_tasks():
    for widget in task_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    for task in tasks:
        task_id, task_name, status = task
        task_label = tk.Label(task_frame, text=f"{task_name} - {status}", font=("Arial", 12))
        task_label.grid(sticky="w", padx=10)

        
        done_button = tk.Button(task_frame, text="Done", command=lambda task_id=task_id: mark_done(task_id))
        done_button.grid(row=tasks.index(task), column=1, padx=10, pady=5)

        delete_button = tk.Button(task_frame, text="Delete", command=lambda task_id=task_id: delete_task(task_id))
        delete_button.grid(row=tasks.index(task), column=2, padx=10, pady=5)


root = tk.Tk()
root.title("To-Do List")


task_entry = tk.Entry(root, width=40, font=("Arial", 12))
task_entry.grid(row=0, column=0, padx=10, pady=10)


add_button = tk.Button(root, text="Add Task", width=20, font=("Arial", 12), command=add_task)
add_button.grid(row=0, column=1, padx=10, pady=10)


task_frame = tk.Frame(root)
task_frame.grid(row=1, column=0, columnspan=2, pady=10)


create_table()
load_tasks()


root.mainloop()
