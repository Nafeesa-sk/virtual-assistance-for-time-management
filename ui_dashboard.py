# ui_dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from backend_task_manager import load_tasks, update_task, delete_task
from backend_class_schedule import load_today_classes
from backend_scheduler import find_free_slots, suggest_slot_for_day
from datetime import datetime, timedelta

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="black")

        tk.Label(self, text="📅 Dashboard – Smart AI Time Manager", font=("Arial", 18, "bold"), bg="black", fg="grey").pack(pady=10)

        # Class Routine
        self.show_classes()

        # Tasks Table
        self.show_tasks()

        # Time Suggestion
        self.show_time_suggestions()

    def show_classes(self):
        class_frame = tk.Frame(self, bg="black")
        class_frame.pack(pady=10)

        tk.Label(class_frame, text="Today's Class Routine:", font=("Arial", 14, "bold"), bg="black", fg="white").pack()

        classes = load_today_classes()
        if not classes.empty:
            for _, row in classes.iterrows():
                info = f"{row['Start Time']} - {row['End Time']} | {row['Subject']}"
                tk.Label(class_frame, text=info, font=("Arial", 12), bg="black", fg="lightblue").pack()
        else:
            tk.Label(class_frame, text="No classes today 🎉", bg="black", fg="gray").pack()

    def show_tasks(self):
        task_frame = tk.Frame(self, bg="black")
        task_frame.pack(pady=10)

        tk.Label(task_frame, text="All Tasks:", font=("Arial", 14, "bold"), bg="black", fg="white").pack()

        self.tree = ttk.Treeview(task_frame, columns=("Date", "Time", "Task", "Status"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack()

        btn_frame = tk.Frame(self, bg="black")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="✅ Mark Completed", bg="gray", command=self.mark_completed).pack(side="left", padx=10)
        tk.Button(btn_frame, text="❌ Delete Task", bg="orange", command=self.delete_task).pack(side="left", padx=10)

        self.load_tasks()

    def load_tasks(self):
        self.tree.delete(*self.tree.get_children())
        df = load_tasks()
        for index, row in df.iterrows():
            self.tree.insert("", "end", iid=index, values=(row["Date"], row["Time"], row["Task"], row["Status"]))

    def mark_completed(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                date = self.tree.item(item)["values"][0]
                time = self.tree.item(item)["values"][1]
                # Prevent Early Completion
                if date == datetime.now().strftime("%Y-%m-%d") and datetime.strptime(time, "%H:%M") > datetime.now():
                    messagebox.showerror("Too Early", "Cannot mark this task as completed before its scheduled time!")
                    return
                update_task(int(item), {"Status": "Completed"})
            self.load_tasks()
            messagebox.showinfo("Updated", "Task marked as completed.")

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                delete_task(int(item))
            self.load_tasks()
            messagebox.showinfo("Deleted", "Task deleted successfully.")

    def show_time_suggestions(self):
        time_frame = tk.Frame(self, bg="black")
        time_frame.pack(pady=10)

        tk.Label(time_frame, text="🧠 Smart Time Suggestions", font=("Arial", 14, "bold"), bg="black", fg="white").pack()

        tk.Button(time_frame, text="🔍 Show Free Time Today", bg="gray", command=self.show_today_slots).pack(pady=3)
        tk.Button(time_frame, text="💡 Suggest Slot for Tomorrow/Specific Day", bg="orange", command=self.suggest_for_any_day).pack(pady=3)

        self.slot_output = tk.Text(time_frame, height=6, width=80, bg="black", fg="lightgreen", font=("Consolas", 10))
        self.slot_output.pack(pady=5)

    def show_today_slots(self):
        self.slot_output.delete("1.0", tk.END)
        slots = find_free_slots()
        if slots:
            self.slot_output.insert(tk.END, "Free Slots Today:\n")
            for start, end in slots:
                self.slot_output.insert(tk.END, f"- {start} to {end}\n")
        else:
            self.slot_output.insert(tk.END, "No free time available today.")

    def suggest_for_any_day(self):
        self.slot_output.delete("1.0", tk.END)

        day = simpledialog.askstring("Enter Date", "Enter Date (YYYY-MM-DD) or 'Tomorrow':")

        if day.lower() == "tomorrow":
            day = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        hours = simpledialog.askinteger("Enter Duration", "How many hours do you need?", minvalue=1, maxvalue=8)

        if not day or not hours:
            return

        suggestion = suggest_slot_for_day(day, duration_minutes=hours * 60)

        if suggestion:
            start, end = suggestion
            self.slot_output.insert(tk.END, f"Suggested Slot for {hours} hour(s) on {day}:\n→ {start} to {end}")
        else:
            self.slot_output.insert(tk.END, f"No available slot for {hours} hour(s) on {day}")
