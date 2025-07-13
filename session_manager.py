import json
import os

SESSION_FILE = "session.json"

def save_session(user_id):
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": user_id}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("user_id")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)