from flask import jsonify, session
from storage import load_json
from config import USERS_FILE
from utils import log_action

def login_user(username, password):
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    users_data = load_json(USERS_FILE)
    users = users_data.get("users", [])

    for user in users:
        if user["username"].lower() == username.lower() and user["password"] == password:
            log_action(username, "Logged in")
            session["username"] = user["username"]
            session["role"] = "admin" if user["username"].lower() == "admin" else "user"
            return jsonify({
                "message": "Login successful",
                "user": {
                    "username": user["username"],
                    "name": user["name"],
                    "tier": user["tier"],
                    "points": user["points"],
                    "referrals": user.get("referrals", []),
                    "role": session["role"]
                }
            })

    return jsonify({"error": "Invalid credentials"}), 401
