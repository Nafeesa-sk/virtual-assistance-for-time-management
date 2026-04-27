# backend_reminder.py

import time
from datetime import datetime
from backend_task_manager import load_tasks
import threading
import tkinter.messagebox as messagebox

def check_and_remind():
    """
    Continuously checks the current time against scheduled tasks.
    If a task is due within 1 minute, shows a popup reminder.
    """
    reminded_tasks = set()

    def run_checker():
        while True:
            now = datetime.now().strftime("%H:%M")
            today = datetime.now().strftime("%Y-%m-%d")
            df = load_tasks()
            for i, row in df.iterrows():
                if row["Date"] == today and row["Time"] == now and row["Task"] not in reminded_tasks:
                    reminded_tasks.add(row["Task"])
                    show_popup(row["Task"])
            time.sleep(60)

    threading.Thread(target=run_checker, daemon=True).start()

def show_popup(task_name):
    try:
        messagebox.showinfo("⏰ Task Reminder", f"It's time for: {task_name}")
    except:
        print(f"Reminder: It's time for {task_name}")
