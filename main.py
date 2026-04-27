# main.py

import tkinter as tk
from ui_dashboard import Dashboard
from ui_add_task import AddTask
from ui_view_tasks import ViewTasks
from ui_stats import Stats
from ui_class_routine import ClassRoutine
from backend_reminder import check_and_remind  # Optional: for reminders

def launch_app():
    root = tk.Tk()
    root.title("Virtual Assistant for Time Management")
    root.geometry("1000x600")
    root.configure(bg='black')

    # Define tabs and their corresponding classes
    tabs = {
        "Dashboard": Dashboard,
        "Add Task": AddTask,
        "View/Edit Tasks": ViewTasks,
        "Productivity Stats": Stats,
        "Class Routine Setup": ClassRoutine
    }

    # Navigation panel on the left
    nav_frame = tk.Frame(root, bg="grey")
    nav_frame.pack(side="left", fill="y")

    # Main content area on the right
    content_frame = tk.Frame(root, bg="black")
    content_frame.pack(side="right", expand=True, fill="both")

    # Store tab instances
    frames = {}

    def show_tab(tab_name):
        for frame in frames.values():
            frame.pack_forget()
        frames[tab_name].pack(fill="both", expand=True)

    # Create buttons for each tab
    for name, FrameClass in tabs.items():
        button = tk.Button(nav_frame, text=name, font=("Arial", 12), bg="tan", fg="black",
                           command=lambda n=name: show_tab(n))
        button.pack(padx=10, pady=10, fill="x")

        # Initialize the frame and hide it
        frames[name] = FrameClass(content_frame)
        frames[name].pack_forget()

    # Start with the Dashboard
    show_tab("Dashboard")

    # Optional: start reminders in the background
    check_and_remind()

    root.mainloop()

if __name__ == "__main__":
    launch_app()
