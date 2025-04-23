import json
import os


def load_json(path):
    """
    Loads data from a JSON file.
    Returns an empty structure (dict or list) if the file doesn't exist.
    """
    if not os.path.exists(path):
        # Infer default structure based on filename
        if path.endswith("users.json"):
            return {"users": []}
        elif path.endswith("referrals.json"):
            return {"referrals": []}
        elif path.endswith("logs.json"):
            return {"logs": []}
        else:
            return {}

    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_json(path, data):
    """
    Saves structured data (dict or list) to a JSON file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
