import pandas as pd
import datetime
import os

ROUTINE_FILE = "routine.csv"

def load_class_routine():
    if os.path.exists(ROUTINE_FILE):
        try:
            df = pd.read_csv(ROUTINE_FILE)
            return df
        except pd.errors.EmptyDataError:
            # Auto create header if file is empty
            df = pd.DataFrame(columns=["Day", "Subject", "Start Time", "End Time"])
            df.to_csv(ROUTINE_FILE, index=False)
            return df
    else:
        return pd.DataFrame(columns=["Day", "Subject", "Start Time", "End Time"])

def load_today_classes():
    today = datetime.datetime.today().strftime("%A")
    df = load_class_routine()
    today_df = df[df["Day"].str.lower() == today.lower()]
    return today_df.sort_values("Start Time")
