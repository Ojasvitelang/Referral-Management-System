from flask import jsonify
from storage import load_json, save_json
from config import USERS_FILE
from utils import log_action, calculate_tier

def create_user(data):
    """
    Adds a new user account. Used by the admin.

    Expected JSON:
    {
        "username": "dr.jane",
        "password": "Secure123",
        "name": "Dr. Jane Doe",
        "gender": "Female",
        "qualification": "MBBS+",
        "courses_done": ["PGDCC", "DFND"],
        "phone": "9876543210",
        "email": "jane@example.com", (optional)
        "city": "Mumbai"
    }
    """
    users = load_json(USERS_FILE).get("users", [])

    # Check for duplicates
    for user in users:
        if user["username"] == data["username"]:
            return jsonify({"error": "Username already exists"}), 400

    # Validation (simple)
    if len(data["password"]) < 8 or not any(c.isupper() for c in data["password"]) or not any(c.isdigit() for c in data["password"]):
        return jsonify({"error": "Password must be at least 8 characters with 1 uppercase and 1 digit"}), 400

    new_user = {
        "username": data["username"],
        "password": data["password"],
        "name": data["name"],
        "gender": data["gender"],
        "qualification": data["qualification"],
        "courses_done": data["courses_done"],
        "phone": data["phone"],
        "email": data.get("email", ""),
        "city": data["city"],
        "tier": "Bronze",
        "points": 0,
        "referrals": []
    }

    users.append(new_user)
    save_json(USERS_FILE, {"users": users})
    log_action("admin", f"Created user {new_user['username']}")

    return jsonify({"message": "User created", "user": new_user})


def list_users():
    """
    Returns all users (admin view).
    """
    users = load_json(USERS_FILE).get("users", [])
    return jsonify({"users": users})


def get_user_info(username):
    """
    Returns the profile and tier/points of a specific user.
    """
    users = load_json(USERS_FILE).get("users", [])
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    profile = {
        "name": user["name"],
        "username": user["username"],
        "points": user.get("points", 0),
        "tier": user.get("tier", "Bronze")
    }
    return jsonify(profile)
