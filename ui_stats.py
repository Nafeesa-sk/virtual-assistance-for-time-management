# ui_stats.py

import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from backend_task_manager import load_tasks

class Stats(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="black")

        tk.Label(self, text="📊 Productivity Stats", font=("Arial", 18, "bold"), bg="black", fg="orange").pack(pady=10)

        self.stats_output = tk.Text(self, height=10, width=80, bg="black", fg="white", font=("Consolas", 10))
        self.stats_output.pack(pady=10)

        tk.Button(self, text="Refresh Stats", font=("Arial", 12), bg="orange", command=self.display_stats).pack(pady=5)
        tk.Button(self, text="Show Pie Chart", font=("Arial", 12), bg="gray", command=self.show_pie_chart).pack(pady=5)

        self.display_stats()

    def display_stats(self):
        df = load_tasks()
        total = len(df)
        completed = len(df[df["Status"] == "Completed"])
        pending = total - completed

        self.stats_output.delete("1.0", tk.END)
        self.stats_output.insert(tk.END, f"Total Tasks     : {total}\n")
        self.stats_output.insert(tk.END, f"Completed Tasks : {completed}\n")
        self.stats_output.insert(tk.END, f"Pending Tasks   : {pending}\n")

        if not df.empty:
            category_counts = df["Category"].value_counts()
            self.stats_output.insert(tk.END, "\nTasks by Category:\n")
            for cat, count in category_counts.items():
                self.stats_output.insert(tk.END, f"  {cat}: {count}\n")

    def show_pie_chart(self):
        df = load_tasks()
        if not df.empty:
            status_counts = df["Status"].value_counts()
            labels = status_counts.index
            sizes = status_counts.values
            plt.figure(figsize=(6, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title("Task Completion Overview")
            plt.axis("equal")
            plt.show()
