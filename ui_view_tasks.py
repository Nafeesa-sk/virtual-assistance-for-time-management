# ui_view_tasks.py

import tkinter as tk
from tkinter import ttk, messagebox
from backend_task_manager import load_tasks, delete_task

class ViewTasks(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="black")

        tk.Label(self, text="📅 View & Edit Tasks", font=("Arial", 18, "bold"), bg="black", fg="orange").pack(pady=10)

        # Include Duration column
        self.tree = ttk.Treeview(
            self,
            columns=("Date", "Time", "Task", "Category", "Priority", "Duration", "Status"),
            show="headings"
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110)

        self.tree.pack(pady=10)

        btn_frame = tk.Frame(self, bg="black")
        btn_frame.pack()

        tk.Button(btn_frame, text="🗑️ Delete Task", bg="orange", command=self.delete_task).pack(side="left", padx=10)

        self.load_tasks()

    def load_tasks(self):
        self.tree.delete(*self.tree.get_children())
        df = load_tasks()
        for index, row in df.iterrows():
            self.tree.insert(
                "", "end", iid=index,
                values=(
                    row["Date"], row["Time"], row["Task"], row["Category"], row["Priority"],
                    row.get("Duration (Hours)", 1), row["Status"]
                )
            )

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                delete_task(int(item))
            self.load_tasks()
            messagebox.showinfo("Deleted", "Task deleted successfully.")
