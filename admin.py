from flask import jsonify
from storage import load_json, save_json
from config import REFERRALS_FILE, USERS_FILE
from utils import update_user_points, log_action
from datetime import datetime

def approve_referral(data):
    """
    Admin approves a referral and marks it as 'Converted'.
    Adds bonus points to the referrer.
    """
    referral_id = data["referral_id"]
    admission_amount = int(data["admission_amount"])

    referrals = load_json(REFERRALS_FILE).get("referrals", [])
    for ref in referrals:
        if ref["id"] == referral_id:
            if ref["status"] == "Converted":
                return jsonify({"error": "Already converted"}), 400

            ref["status"] = "Converted"
            ref["converted_at"] = datetime.utcnow().strftime("%Y-%m-%d")
            ref["admission_amount"] = admission_amount

            # Points: 250 + 1% of admission
            base = 250
            bonus = int(admission_amount * 0.01)
            total = base + bonus
            ref["points_awarded"] += total

            save_json(REFERRALS_FILE, {"referrals": referrals})
            update_user_points(ref["referrer"], total)
            log_action("admin", f"Approved {referral_id}, +{total} pts to {ref['referrer']}")

            return jsonify({"message": "Referral approved", "points_awarded": total})

    return jsonify({"error": "Referral not found"}), 404


def reject_referral(data):
    """
    Admin rejects a referral and removes any previously awarded points.
    """
    referral_id = data["referral_id"]

    referrals = load_json(REFERRALS_FILE).get("referrals", [])
    for ref in referrals:
        if ref["id"] == referral_id:
            if ref["status"] == "Rejected":
                return jsonify({"error": "Already rejected"}), 400

            ref["status"] = "Rejected"
            points = ref.get("points_awarded", 0)
            save_json(REFERRALS_FILE, {"referrals": referrals})
            update_user_points(ref["referrer"], -points)
            log_action("admin", f"Rejected {referral_id}, -{points} pts from {ref['referrer']}")

            return jsonify({"message": "Referral rejected", "points_removed": points})

    return jsonify({"error": "Referral not found"}), 404


def add_points(username, points, reason):
    """
    Admin manually adjusts user points.
    """
    users = load_json(USERS_FILE).get("users", [])
    for user in users:
        if user["username"] == username:
            user["points"] += points
            save_json(USERS_FILE, {"users": users})
            log_action("admin", f"Adjusted {points} pts to {username}: {reason}")
            return jsonify({"message": "Points adjusted", "points": points})

    return jsonify({"error": "User not found"}), 404


def generate_report(start_date, end_date):
    """
    Generates report of referrals in given date range.
    """
    referrals = load_json(REFERRALS_FILE).get("referrals", [])
    filtered = [r for r in referrals if start_date <= r["created_at"] <= end_date]
    return jsonify({"report": filtered})
