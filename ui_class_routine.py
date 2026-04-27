# ui_class_routine.py

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

ROUTINE_FILE = "routine.csv"

class ClassRoutine(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="black")

        tk.Label(self, text="📘 Set Class Routine", font=("Arial", 18, "bold"), bg="black", fg="orange").pack(pady=10)

        form_frame = tk.Frame(self, bg="black")
        form_frame.pack(pady=5)

        self.entries = {}
        fields = ["Day", "Subject", "Start Time", "End Time"]
        for i, label in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Arial", 12), bg="black", fg="white").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[label] = entry

        tk.Button(self, text="Save Entry", bg="orange", font=("Arial", 12),
                  command=self.save_entry).pack(pady=10)

        self.routine_display = tk.Text(self, height=10, width=80, bg="black", fg="white", font=("Consolas", 10))
        self.routine_display.pack(pady=5)

        self.load_routine()

    def save_entry(self):
        entry = {key: self.entries[key].get() for key in self.entries}
        if "" in entry.values():
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        df = pd.DataFrame([entry])
        if os.path.exists(ROUTINE_FILE):
            df.to_csv(ROUTINE_FILE, mode='a', header=False, index=False)
        else:
            df.to_csv(ROUTINE_FILE, index=False)

        messagebox.showinfo("Saved", "Class routine entry added.")
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.load_routine()

    def load_routine(self):
        self.routine_display.delete("1.0", tk.END)
        if os.path.exists(ROUTINE_FILE):
            df = pd.read_csv(ROUTINE_FILE)
            if not df.empty:
                self.routine_display.insert(tk.END, df.to_string(index=False))
            else:
                self.routine_display.insert(tk.END, "No routine entries yet.")
        else:
            self.routine_display.insert(tk.END, "No routine file found.")
