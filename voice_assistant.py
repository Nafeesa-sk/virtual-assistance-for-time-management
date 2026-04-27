# voice_assistant.py

import speech_recognition as sr
import re

def listen_for_task():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak your task like:")
        print("Example: Study Maths for 2 hours on 2025-04-17 at 17:00")

        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("Recognized:", text)

        task = ""
        duration = "1"
        date = ""
        time = ""

        # Extract Duration
        duration_match = re.search(r'for (\d+) hour', text)
        if duration_match:
            duration = duration_match.group(1)

        # Extract Date
        date_match = re.search(r'on (\d{4}-\d{2}-\d{2})', text)
        if date_match:
            date = date_match.group(1)

        # Extract Time
        time_match = re.search(r'at (\d{1,2}:\d{2})', text)
        if time_match:
            time = time_match.group(1)

        # Extract Task Name
        task_part = text.split('for')[0].split('on')[0].split('at')[0].strip()
        task = task_part

        return {
            "task": task,
            "duration": duration,
            "date": date,
            "time": time
        }

    except Exception as e:
        print("Error:", e)
        return None
