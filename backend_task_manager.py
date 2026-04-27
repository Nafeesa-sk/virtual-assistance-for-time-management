# backend_task_manager.py

import pandas as pd
import os
from datetime import datetime

TASK_FILE = "tasks.csv"

def load_tasks():
    if os.path.exists(TASK_FILE):
        try:
            return pd.read_csv(TASK_FILE)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["Date", "Time", "Task", "Category", "Priority", "Status"])
            df.to_csv(TASK_FILE, index=False)
            return df
    else:
        return pd.DataFrame(columns=["Date", "Time", "Task", "Category", "Priority", "Status"])

def save_tasks(df):
    df.to_csv(TASK_FILE, index=False)

def add_task(task_data):
    df = load_tasks()
    df = pd.concat([df, pd.DataFrame([task_data])], ignore_index=True)
    save_tasks(df)

def delete_task(index):
    df = load_tasks()
    df.drop(index, inplace=True)
    save_tasks(df)

def update_task(index, updated_data):
    df = load_tasks()
    for key, value in updated_data.items():
        df.at[index, key] = value
    save_tasks(df)

def load_tasks_for_today():
    df = load_tasks()
    today = datetime.now().strftime("%Y-%m-%d")
    df_today = df[df["Date"] == today]
    return df_today.sort_values("Time")
