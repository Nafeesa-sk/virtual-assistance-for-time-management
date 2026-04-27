# backend_scheduler.py

from datetime import datetime, timedelta
from backend_class_schedule import load_class_routine
from backend_task_manager import load_tasks

def get_events_for_day(date_str):
    routine_df = load_class_routine()
    tasks_df = load_tasks()

    class_events = []
    if not routine_df.empty:
        class_rows = routine_df[routine_df["Day"] == date_str]
        class_events = [
            (datetime.strptime(row["Start Time"], "%H:%M").time(),
             datetime.strptime(row["End Time"], "%H:%M").time())
            for _, row in class_rows.iterrows()
        ]

    task_time_blocks = []
    if not tasks_df.empty:
        task_rows = tasks_df[tasks_df["Date"] == date_str]
        for _, row in task_rows.iterrows():
            try:
                duration = int(row.get("Duration (Hours)", 1))
            except:
                duration = 1
            start = datetime.strptime(row["Time"], "%H:%M")
            end = start + timedelta(hours=duration)
            task_time_blocks.append((start.time(), end.time()))

    all_events = class_events + task_time_blocks
    return sorted(all_events, key=lambda x: x[0])

def find_free_slots_for_day(date_str, duration_minutes=30):
    events = get_events_for_day(date_str)

    # Use full 24-hour day if needed
    day_start = datetime.strptime("00:00", "%H:%M").time()
    day_end = datetime.strptime("23:59", "%H:%M").time()

    free_slots = []
    current = day_start

    for start, end in events:
        if start > current:
            gap = datetime.combine(datetime.today(), start) - datetime.combine(datetime.today(), current)
            if gap.total_seconds() >= duration_minutes * 60:
                free_slots.append((current.strftime("%H:%M"), start.strftime("%H:%M")))
        current = max(current, end)

    if current < day_end:
        gap = datetime.combine(datetime.today(), day_end) - datetime.combine(datetime.today(), current)
        if gap.total_seconds() >= duration_minutes * 60:
            free_slots.append((current.strftime("%H:%M"), day_end.strftime("%H:%M")))

    return free_slots

def suggest_slot_for_day(date_str, duration_minutes=60):
    slots = find_free_slots_for_day(date_str, duration_minutes)
    return slots[0] if slots else None

def find_free_slots():
    today = datetime.now().strftime("%Y-%m-%d")
    return find_free_slots_for_day(today, 30)
