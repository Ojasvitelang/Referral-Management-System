from storage import load_json, save_json
from config import USERS_FILE, LOGS_FILE, TIERS
from datetime import datetime

def log_action(user, action):
    """
    Appends a log entry with the username and action taken.
    """
    logs = load_json(LOGS_FILE).get("logs", [])
    logs.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": user,
        "action": action
    })
    save_json(LOGS_FILE, {"logs": logs})

def get_user(username):
    """
    Returns a user dictionary by username.
    """
    users = load_json(USERS_FILE).get("users", [])
    return next((u for u in users if u["username"] == username), None)

def update_user_points(username, delta):
    """
    Updates a user's points and recalculates their tier.
    """
    users_data = load_json(USERS_FILE)
    users = users_data.get("users", [])
    updated = False

    for user in users:
        if user["username"] == username:
            user["points"] += delta
            user["tier"] = calculate_tier(user["points"])
            updated = True
            break

    if updated:
        save_json(USERS_FILE, {"users": users})
    else:
        print(f"[Warning] update_user_points: User '{username}' not found.")

def calculate_tier(points):
    """
    Determines the tier based on point thresholds.
    """
    for tier in TIERS:
        if points >= tier["min_points"]:
            return tier["name"]
    return "Bronze"
