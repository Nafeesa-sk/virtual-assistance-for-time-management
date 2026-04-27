# ui_add_task.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import pandas as pd
from backend_task_manager import add_task, load_tasks
from backend_scheduler import suggest_slot_for_day
from voice_assistant import listen_for_task

class AddTask(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="black")

        tk.Label(self, text="➕ Add New Task", font=("Arial", 18, "bold"), bg="black", fg="orange").pack(pady=10)

        form_frame = tk.Frame(self, bg="black")
        form_frame.pack(pady=10)

        labels = ["Task", "Date (YYYY-MM-DD)", "Time (HH:MM)", "Category", "Priority", "Duration (Hours)"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, font=("Arial", 12), bg="black", fg="white").grid(row=i, column=0, sticky="e", pady=5)
            entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[label] = entry

        self.entries["Priority"].insert(0, "Medium")

        tk.Button(self, text="Add Task", bg="orange", fg="black", font=("Arial", 12),
                  command=self.save_task).pack(pady=10)

        tk.Button(self, text="🎤 Voice Input", bg="gray", fg="white", font=("Arial", 11),
                  command=self.voice_input).pack(pady=5)

        tk.Button(self, text="💡 Suggest Free Slot", bg="green", fg="white", font=("Arial", 11),
                  command=self.suggest_time).pack(pady=5)

    def suggest_time(self):
        date = self.entries["Date (YYYY-MM-DD)"].get()
        if not date:
            messagebox.showerror("Missing Date", "Enter date first!")
            return
        hours = simpledialog.askinteger("Duration", "How many hours?", minvalue=1, maxvalue=8)
        if not hours:
            return

        suggestion = suggest_slot_for_day(date, hours * 60)
        if suggestion:
            start, end = suggestion
            self.entries["Time (HH:MM)"].delete(0, tk.END)
            self.entries["Time (HH:MM)"].insert(0, start)
            self.entries["Duration (Hours)"].delete(0, tk.END)
            self.entries["Duration (Hours)"].insert(0, hours)
            messagebox.showinfo("Suggested Slot", f"Suggested Time: {start} to {end}")
        else:
            messagebox.showinfo("No Slot", "No available free slot for given hours.")

    def save_task(self):
        task_data = {
            "Task": self.entries["Task"].get(),
            "Date": self.entries["Date (YYYY-MM-DD)"].get(),
            "Time": self.entries["Time (HH:MM)"].get(),
            "Category": self.entries["Category"].get(),
            "Priority": self.entries["Priority"].get(),
            "Status": "Pending",
        }

        duration_hours = self.entries["Duration (Hours)"].get()

        if not all(task_data.values()) or not duration_hours:
            messagebox.showerror("Missing Fields", "All fields are required!")
            return

        try:
            task_date = datetime.strptime(task_data["Date"], "%Y-%m-%d")
            task_time = datetime.strptime(task_data["Time"], "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Format", "Enter date/time correctly.")
            return

        # Prevent adding task in past time
        now = datetime.now()
        if task_date.date() == now.date() and task_time.time() <= now.time():
            messagebox.showerror("Invalid Time", "Cannot add task in the past!")
            return

        # Prevent Overlapping Tasks
        df = load_tasks()
        new_start = task_time
        new_end = task_time + timedelta(hours=int(duration_hours))

        for _, row in df.iterrows():
            if row["Date"] == task_data["Date"]:
                existing_start = datetime.strptime(row["Time"], "%H:%M")
                existing_end = existing_start + timedelta(hours=1 if "Duration (Hours)" not in row or pd.isna(row["Duration (Hours)"]) else int(row["Duration (Hours)"]))

                # Check overlap
                if new_start < existing_end and existing_start < new_end:
                    messagebox.showerror("Time Overlap", "This time overlaps with another task!")
                    return

        task_data["Duration (Hours)"] = duration_hours

        add_task(task_data)
        messagebox.showinfo("Success", "Task added successfully!")

        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def voice_input(self):
        result = listen_for_task()
        if result:
            self.entries["Task"].insert(0, result.get("task", ""))
            self.entries["Date (YYYY-MM-DD)"].insert(0, result.get("date", ""))
            self.entries["Time (HH:MM)"].insert(0, result.get("time", ""))
            self.entries["Duration (Hours)"].insert(0, result.get("duration", "1"))

