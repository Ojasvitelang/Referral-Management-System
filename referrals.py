from flask import jsonify
from storage import load_json, save_json
from config import REFERRALS_FILE, USERS_FILE, POINTS_REFERRAL, POINTS_CONVERSION, REVENUE_BONUS_RATE
from utils import log_action, update_user_points
from datetime import datetime
import csv
from io import StringIO


def add_referral(data):
    """
    Adds a new referral and awards referral points.
    """
    referrals = load_json(REFERRALS_FILE).get("referrals", [])

    # Check for duplicates (name, phone, or email)
    for ref in referrals:
        if (
                ref["name"] == data["name"] or
                ref["phone"] == data["phone"] or
                (data.get("email") and ref.get("email") == data["email"])
        ):
            return jsonify({"error": "Duplicate referral"}), 400

    referral_id = f"ref_{len(referrals) + 1:03d}"
    referral = {
        "id": referral_id,
        "referrer": data["referrer"],
        "name": data["name"],
        "phone": data["phone"],
        "email": data.get("email", ""),
        "qualification": data["qualification"],
        "relationship": data["relationship"],
        "course_interested": data["course_interested"],
        "city": data["city"],
        "status": "Pending",
        "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
        "points_awarded": POINTS_REFERRAL
    }

    referrals.append(referral)
    save_json(REFERRALS_FILE, {"referrals": referrals})
    update_user_points(data["referrer"], POINTS_REFERRAL)
    log_action(data["referrer"], f"Submitted referral {referral_id}")

    return jsonify({"message": "Referral added", "referral": referral})


# Alias for compatibility with app.py
submit_referral = add_referral


def convert_referral(data):
    """
    Converts a referral to 'Converted' and adds bonus points.
    """
    referral_id = data["referral_id"]
    admission_amount = int(data["admission_amount"])
    referrals = load_json(REFERRALS_FILE).get("referrals", [])

    for ref in referrals:
        if ref["id"] == referral_id:
            if ref["status"] == "Converted":
                return jsonify({"error": "Referral already converted"}), 400

            ref["status"] = "Converted"
            ref["converted_at"] = datetime.utcnow().strftime("%Y-%m-%d")
            ref["admission_amount"] = admission_amount

            bonus = POINTS_CONVERSION + int(admission_amount * REVENUE_BONUS_RATE)
            ref["points_awarded"] += bonus

            save_json(REFERRALS_FILE, {"referrals": referrals})
            update_user_points(ref["referrer"], bonus)
            log_action("admin", f"Converted {referral_id}, added {bonus} pts to {ref['referrer']}")

            return jsonify({"message": "Referral converted", "points_awarded": bonus})

    return jsonify({"error": "Referral not found"}), 404


def reject_referral(data):
    """
    Marks a referral as rejected and removes awarded points.
    """
    referral_id = data["referral_id"]
    referrals = load_json(REFERRALS_FILE).get("referrals", [])

    for ref in referrals:
        if ref["id"] == referral_id:
            if ref["status"] == "Rejected":
                return jsonify({"error": "Referral already rejected"}), 400

            ref["status"] = "Rejected"
            deducted = ref.get("points_awarded", 0)
            save_json(REFERRALS_FILE, {"referrals": referrals})
            update_user_points(ref["referrer"], -deducted)
            log_action("admin", f"Rejected {referral_id}, removed {deducted} pts")

            return jsonify({"message": "Referral rejected", "points_removed": deducted})

    return jsonify({"error": "Referral not found"}), 404


def get_user_referrals(username):
    """
    Returns all referrals submitted by a specific user.
    """
    referrals = load_json(REFERRALS_FILE).get("referrals", [])
    user_referrals = [r for r in referrals if r["referrer"] == username]
    return jsonify({"referrals": user_referrals})


def upload_referrals_csv(file, username):
    """
    Uploads and processes referrals from a CSV file.
    Awards 50 points per valid referral.
    """
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV."}), 400

    csv_data = file.read().decode('utf-8')
    csv_reader = csv.DictReader(StringIO(csv_data))

    required_fields = {"name", "phone", "city", "relationship", "qualification", "course_interested"}
    added, duplicates, errors = 0, 0, 0

    for row in csv_reader:
        if not required_fields.issubset(row.keys()):
            errors += 1
            continue

        referral = {
            "referrer": username,
            "name": row["name"],
            "phone": row["phone"],
            "email": row.get("email", ""),
            "qualification": row["qualification"],
            "relationship": row["relationship"],
            "course_interested": row["course_interested"],
            "city": row["city"]
        }

        result = add_referral(referral)
        if isinstance(result, tuple) and result[1] == 400:
            duplicates += 1
        else:
            added += 1

    return jsonify({
        "message": f"{added} referrals added. {duplicates} duplicates skipped. {errors} rows invalid."
    })
